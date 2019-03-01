from django.db import models
from django.utils.translation import ugettext_lazy as _

from utils.make_query import make_page
from utils.base_model import BaseModel

# Create your models here.
class DoubanMovie(BaseModel, models.Model):

	id = models.CharField(_('主键ID'), max_length=32, primary_key=True, blank=False)
	douban_movie_id = models.CharField(_('豆瓣电影ID'), max_length=100, blank=False, default='')
	title = models.CharField(_('电影标题'), max_length=500, blank=False, default='')
	cover = models.CharField(_('电影封面图片地址'), max_length=500, blank=True)
	directors = models.CharField(_('导演，多个导演之间用/分割'), max_length=500, blank=True)
	writers = models.CharField(_('编剧，多个编剧之间用/分割'), max_length=500, blank=True)
	actors = models.CharField(_('主演，多个主演之间用/分割'), max_length=2000, blank=True)
	type = models.CharField(_('类型，多个类型之间用/分割'), max_length=500, blank=True)
	area = models.CharField(_('制片国家/地区'), max_length=500, blank=True)
	lang = models.CharField(_('语言'), max_length=100, blank=True)
	release_date = models.DateField(_('上映日期。多个上映日期则选择最新的上映日期'), blank=True, null=True)
	runtime = models.IntegerField(_('片长（分钟）'), blank=True, null=True)
	imdb = models.CharField(_('imdb链接'), max_length=100, blank=True)
	rate = models.FloatField(_('电影评分'), blank=True, null=True)
	votes = models.IntegerField(_('电影评分投票人数'), blank=True, null=True)
	summary = models.CharField(_('电影简介'), max_length=2000, blank=True)

	class Meta:
		db_table = 't_douban_movie'

	def get_conditions(search_key=''):

		filter_by = 'title contains "{search_key}" || actors contains "{search_key}"'.format(search_key=search_key) if search_key else ''

		types = DoubanMovie.get_distinct_with_split('type', '/', filter_by=filter_by, compute_count=True, return_sorted_list=True)
		langs = DoubanMovie.get_distinct_with_split('lang', '/', filter_by=filter_by, compute_count=True, return_sorted_list=True)

		return types, langs