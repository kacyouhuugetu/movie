from django.urls import reverse
from django.http import HttpResponseRedirect

def check_login(need_login=True, redirect='user:to_login', reverse_kwargs=None):
	"""
		用于装饰view函数的装饰器。check_login会根据参数need_login检查用户的登录状态，若检查到不满足登录条件，则跳转至参数redirect指定的url

		参数
		________
			:need_login
				布尔值，表示用户是否需要登录。默认为True，即用户需要登录
			:redirect
				字符串，若检查到不满足登录条件，则将跳转至reverse(redirect)对应的url
			:reverse_kwargs
				字典，将作为reverse函数的kwargs参数

	"""
	def check_login_(func):
		def check_login__(request, *args, **kwargs):
			is_logined = request.user.is_authenticated
			# 重定向
			if ( need_login and not is_logined ) or ( not need_login and is_logined ):
				return HttpResponseRedirect(reverse(redirect, kwargs=reverse_kwargs))
			return func(request, *args, **kwargs)

		return check_login__
	return check_login_