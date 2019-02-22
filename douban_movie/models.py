from django.db import models
from django.utils.translation import ugettext_lazy as _

from utils.make_query import make_page

# Create your models here.
class DoubanMovie(models.Model):

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

	def __str__(self):
		return '%s(%d,%d)'%(self.title, self.rate, self.votes)

	def get_movie(filter_by=None, order_by=None, limit=20, page=1):
		"""
			获取满足条件的影片QuerySet
			
			参数
			_______
				:filter_by
					表示筛选条件的字符串。多个筛选条件之间用&&分割。筛选条件的格式为field op value，其中field表示字段名，op表示操作符，value为值
				:order_by
					表示排序方法的字符串。多个排序方法之间用,分割。排序方法的格式为field direction，其中direction表示排序方向，asc表示正序，desc表示倒序，若不给出则默认为正序
				:limit
					整数。用于分页，与参数page一起使用，表示每一页的大小。若limit为None，则不开启分页。默认为20
				:page
					整数。用于分页，与参数limit一起使用，表示页码。若page为None，则不开启分页。默认为1
			
			返回值
			_______
				表示结果集的QuerySet

			示例
			_______
				假设我们要获取评分为8分以上（不包括8分），且评分人数大于等于100，结果按评分人数倒序，则我们可以如下调用
					>>> filter_by = 'rate > 8 && votes >= 100'
					>>> order_by = 'votes desc'
					>>> result = DoubanMovie.get_movie(filter_by, order_by)

		"""


		return make_page(DoubanMovie, filter_by, order_by, limit, page)

