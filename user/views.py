from django.shortcuts import render
from django.views.decorators.http import require_http_methods, require_GET, require_POST
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout

from user.decorators import check_login

from re import compile, match

main_page_url = 'douban_movie:index'

# Create your views here.
@check_login(False, main_page_url)
@require_GET
def to_register(request):
	return render(request, 'user/register.html')

@require_POST
def register(request):

	if request.user.is_authenticated:
		return JsonResponse({
			'fail_field' : '已登录',
			'msg' : '已登录'
		})

	fail_field, msg = check_regist(**request.POST)
	
	# 注册错误
	if fail_field:
		pass
	
	# 注册成功
	else:
		user = User.objects.create_user(username=request.POST['username'], password=request.POST['password'], email=request.POST['email'])
		user.save()

	return JsonResponse({
		'fail_field' : fail_field,
		'msg' : msg
	})


@check_login(False, main_page_url)
@require_GET
def to_login(request):
	return render(request, 'user/login.html')

@require_POST
def login(request):

	if request.user.is_authenticated:
		return JsonResponse({
			'flag' : 'FAIL',
			'msg' : '已登录'
		})

	flag = 'FAIL'
	msg = '登录失败'


	try:
		username_email = request.POST['username_email']
		password = request.POST['password']
		user = authenticate(request, username=username_email, password=password)

		# 登录失败
		if user is None:
			print('nono')
			pass
		else:
			auth_login(request, user)
			flag, msg = 'SUCCESS', ''

	except:
		pass

	return JsonResponse({
		'flag' : flag,
		'msg' : msg
	})

def logout(request):

	auth_logout(request)
	return HttpResponseRedirect(reverse('user:to_login'))

username_pattern = compile(r'^.{5,10}$')
password_pattern = compile(r'[a-zA-Z0-9_]{8,20}')
email_pattern = compile(r'^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$')

def check_regist(**user_info):

	fail_field = 'unknowned'
	msg = '未知错误'

	print(user_info)

	try:
		if not 'username' in user_info:
			fail_field = 'username'
			msg = '用户名不能为空'
		if not 'password' in user_info:
			fail_field = 'password'
			msg = '密码不能为空'

		username = user_info['username'][0]
		password = user_info['password'][0]
		email = user_info['email'][0] if len(user_info['email'])==1 else ''

		print(match(username_pattern, username))
		print(len(User.objects.filter(username=username)))
		# 检查用户名是否合法
		if not match(username_pattern, username):
			fail_field = 'username'
			msg = '用户名需为5到10个字符'

		# 检查邮箱是否合法
		elif email and not match(email_pattern, email):
			fail_field = 'email'
			msg = '邮箱格式错误'

		elif len(User.objects.filter(username=username))>0:
			fail_field = 'username'
			msg = '已存在的用户名'

		elif email and len(User.objects.filter(email=email))>0:
			fail_field = 'email'
			msg = '已存在的邮箱'
		else:
			fail_field = ''
			msg = '成功'


	except:
		pass

	return fail_field, msg

