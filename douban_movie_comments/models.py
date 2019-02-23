from django.db import models
from django_comments.abstracts import CommentAbstractModel
from django.utils.translation import ugettext_lazy as _


from utils.make_query import make_page


# Create your models here.

class DoubanMovieComments(CommentAbstractModel):
	replyComment = models.DecimalField(_('回复评论ID'), max_digits=11, decimal_places=0)

	class Meta:
		db_table = 't_douban_movie_comments'

	def get_comments(filter_by=None, order_by=None, limit=20, page=1):
		"""
			获取满足条件的评论QuerySet
			
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


		return DoubanMovieComments(DoubanMovie, filter_by, order_by, limit, page)
