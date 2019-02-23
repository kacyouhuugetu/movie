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
from user.views import to_register, register, to_login, login, logout

app_name = 'user'

urlpatterns = [
	path('to_register', to_register, name='to_register'),
	path('register', register, name='register'),
	path('to_login', to_login, name='to_login'),
	path('login', login, name='login'),
    path('logout', logout, name='logout')
]
