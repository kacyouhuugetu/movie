from django.shortcuts import render
from django.views.decorators.http import require_http_methods, require_GET, require_POST
from django.http import HttpResponse, JsonResponse

from user.decorators import check_login
from douban_movie.models import DoubanMovie
from datetime import date

# Create your views here.

@check_login()
@require_GET
def test(request):

	return render(request, 'douban_movie/test.html')

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
