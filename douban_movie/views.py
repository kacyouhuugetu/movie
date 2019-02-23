from django.shortcuts import render
from django.views.decorators.http import require_http_methods, require_GET, require_POST
from django.http import HttpResponse, JsonResponse

from user.decorators import check_login
from douban_movie.models import DoubanMovie


# Create your views here.

@check_login()
@require_GET
def test(request):

	return render(request, 'douban_movie/test.html')