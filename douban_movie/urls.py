"""movie URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from douban_movie.views import index, movie_detail, search_movie, to_search_list

app_name = 'douban_movie'

urlpatterns = [
	path('', index, name='index'),
	path('movie_detail', movie_detail, name='movie_detail'),
	path('movie_detail/<str:id>', movie_detail, name='movie_detail'),
	path('search_movie', search_movie, name='search_movie'),
	path('to_search_list', to_search_list, name='to_search_list'),

]
