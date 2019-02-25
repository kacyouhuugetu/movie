from re import split as re_split
from datetime import date, datetime

def make_page(model, filter_by=None, order_by=None, limit=20, page=1, compute_count=False, to_serializable=True):

	selector = model.objects

	filter_by_kwargs = {}
	exclude_kwargs = {}
	order_by_args = []

	if filter_by:
		for field_op_value in filter_by.split('&&'):

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
				exclude_kwargs[field[1:]+suffix] = value
			else:
				filter_by_kwargs[field+suffix] = value

		if filter_by_kwargs:
			selector = selector.filter(**filter_by_kwargs)
		if exclude_kwargs:
			selector = selector.exclude(**exclude_kwargs)

	if order_by:
		for field_direction in order_by.split(','):

			field, *direction = [ele.strip() for ele in re_split(r'\s+', field_direction.strip(), maxsplit=1)]
			direction = direction[0] if direction else 'asc'
			direction = '-' if direction=='desc' else ''
			order_by_args.append(direction + field)

		selector = selector.order_by(*order_by_args)

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
			data.append(item.to_dict())
	else:
		data = selector

	return count, data