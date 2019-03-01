from django.shortcuts import render
from django.views.decorators.http import require_http_methods, require_GET, require_POST
from django.http import HttpResponse, JsonResponse, Http404

from user.decorators import check_login
from douban_movie.models import DoubanMovie
from datetime import date

# Create your views here.

@check_login()
@require_GET
def index(request):

	today = date.today()
	y, m, d = today.year, today.month, today.day

	filter_by = 'release_date > date({last_year},{month},{day}) && ~votes = None && ~rate = None'.format(
		last_year = y - 1,
		month = m,
		day = d
	)
	order_by = 'votes desc, rate desc'

	_,data =  DoubanMovie.make_page(filter_by, order_by, page=1, limit=5, compute_count=False)

	context = {
		'movies' : data
	}

	return render(request, 'douban_movie/index.html', context)


@require_GET
def movie_detail(request, id):
	if not id:
		raise Http404('电影id不可为空')

	filter_by = 'id == "%s"'%str(id)
	_, data = DoubanMovie.make_page(filter_by=filter_by, limit=1, page=1, compute_count=False, to_serializable=True)

	data = data[0] if len(data)>0 else {}

	return render(request, 'douban_movie/movie_detail.html', {
		'movie' : data
	})

@require_GET
def to_search_list(request):

	search_key = request.GET.get('search_key', '')

	context = {'search_key' : search_key} if search_key else None

	return render(request, 'douban_movie/search_list.html', context)

@require_GET
def search_movie(request):
	args = request.GET
	search_key = args.get('search_key', '')
	page = int(args.get('page', 1))
	limit = int(args.get('limit', 20))
	order_by = args.get('order_by', 'release_date desc')

	filter_by = 'title contains "{search_key}" || actors contains "{search_key}"'.format(search_key=search_key) if search_key else None

	count, data = DoubanMovie.make_page(filter_by, order_by, page=page, limit=limit, to_serializable=True, compute_count=True)

	types, langs = DoubanMovie.get_conditions(search_key)

	context = {
		'npage' : count//limit + (1 if count%limit!=0 else 0),
		'page' : page,
		'movies' : data,
		'conditions' : {
			'types' : types,
			'langs' : langs
		}
	}
	return render(request, 'douban_movie/search_list.html', context)