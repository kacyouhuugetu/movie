from django.shortcuts import render

from navigation.models import Navigation
from django.http import JsonResponse

# Create your views here.
def get_navigation(request):
	return JsonResponse(Navigation.make_tree(filter_by='ismenu = True', order_by='level	,order'), safe=False, json_dumps_params={'ensure_ascii':False})