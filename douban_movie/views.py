from django.shortcuts import render
from django.http import HttpResponse

from douban_movie.models import DoubanMovie
# Create your views here.

def test(request):

	return HttpResponse("Hello, world. You're at the polls index.")