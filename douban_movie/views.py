from django.shortcuts import render
from django.views.decorators.http import require_http_methods, require_GET, require_POST
from django.http import HttpResponse, JsonResponse, Http404

from user.decorators import check_login
from douban_movie.models import DoubanMovie
from datetime import date

# Create your views here.

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

	if not search_key:
		raise Http404('搜索关键字必须非空')

	return render(request, 'douban_movie/search_list.html', {'search_key' : search_key})


def search_movie(request):
	args = request.GET
	search_key = args.get('search_key', '')
	page = args.get('page', '')
	limit = args.get('limit', '')
	order_by = args.get('order_by', 'release_date desc')
	compute_count = args.get('compute_count', False)

	if not search_key:
		return JsonResponse({
			'flag' : 'FAIL',
			'msg' : '请输入搜索关键字'
		}, json_dumps_params={'ensure_ascii':False})

	try:
		filter_by = 'title contains "{search_key}" || actors contains "{search_key}"'.format(search_key=search_key)
		count, data = DoubanMovie.make_page(filter_by, order_by, page=page, limit=limit, compute_count=compute_count)

	except:
		return JsonResponse({
			'flag' : 'FAIL',
			'msg' : '未知错误'
		}, json_dumps_params={'ensure_ascii':False})

	return JsonResponse({
		'flag' : 'SUCCESS',
		'msg' : '',
		'count' : count,
		'data' : data
	}, json_dumps_params={'ensure_ascii':False})

