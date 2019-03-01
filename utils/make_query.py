from re import split as re_split
from datetime import date, datetime

from django.db.models import Q
from django.db.utils import NotSupportedError
from django.db.models import Count

def make_selector(model, filter_by=None, order_by=None):
	selector = model.objects

	order_by_args = []

	if filter_by:

		splitor = '&&' if '&&' in filter_by else '||'

		Qs = []
		for field_op_value in filter_by.split(splitor):

			field, op, value = [ele.strip() for ele in re_split(r'\s+', field_op_value.strip(), maxsplit=2)]
			suffix = '' if op in ('=','==') else \
					'__gt' if op == '>' else \
					'__gte' if op == '>=' else \
					'__lt' if op == '<' else \
					'__lte' if op == '<=' else \
					'__'+op if op in ('in','contains','icontains','startswith','istartswith','endswith','iendswith','year','month','day') else \
					None

			if suffix is None:
				raise ValueError('不可识别的操作符：%s'%str(suffix))

			value = eval(value)

			if field[0] == '~':
				Qs.append(~Q(**{field[1:]+suffix:value}))
			else:
				Qs.append(Q(**{field+suffix:value}))

		final_Q = Qs[0]
		for Q_ in Qs[1:]:
			if splitor == '&&':
				final_Q = final_Q & Q_
			else:
				final_Q = final_Q | Q_

		selector = selector.filter(final_Q)


	if order_by:
		for field_direction in order_by.split(','):

			field, *direction = [ele.strip() for ele in re_split(r'\s+', field_direction.strip(), maxsplit=1)]
			direction = direction[0] if direction else 'asc'
			direction = '-' if direction=='desc' else ''
			order_by_args.append(direction + field)

		selector = selector.order_by(*order_by_args)

	return selector


def make_page(model, filter_by=None, order_by=None, limit=20, page=1, compute_count=False, to_serializable=True, show_cols=None):

	selector = make_selector(model, filter_by, order_by)

	if not show_cols is None:
		selector = selector.values(*show_cols)

	if not filter_by and not order_by:
		selector = selector.all()

	count = len(selector) if compute_count else 0

	# 开启分页
	if page and limit:
		page, limit = int(page), int(limit)
		selector = selector[(page-1)*limit:page*limit]

	data = []
	if to_serializable:
		for item in selector:
			data.append(item if type(item)==dict else item.to_dict())
	else:
		data = selector

	return count, data


def get_distinct(model, col, filter_by=None, compute_count=False):
	
	selector = make_selector(model, filter_by).values(col)

	if compute_count:
		res = selector.annotate(count = Count(col))
	else:
		res =  selector.distinct()

	return res