from navigation.models import Navigation


def navigation(request):
	"""
		向模板中添加导航信息
	"""

	urls = []
	for navigation in Navigation.make_page(page=None)[1]:
		if navigation.get('url'):
			urls.append(navigation.url)

	return {'navigation_urls': urls}