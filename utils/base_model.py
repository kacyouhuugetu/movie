from django.core.exceptions import FieldDoesNotExist

from utils.make_query import make_page
from utils.common import list_to_tree

class BaseModel:
	"""
		若继承本类，需同时继承类django.db.models.Model
	"""
	__fields = None

	def __load_fields(self):
		if self.__fields is None:
			self.__fields = [field.name for field in self._meta.get_fields()]

	def keys(self):
		"""
			返回模型所有字段名的列表
		"""
		self.__load_fields()

		return self.__fields

	def get(self, key, default=None):
		"""
			根据字段名返回值。若字段不存在，则引发django.core.exceptions.FieldDoesNotExist异常
		"""
		self.__load_fields()

		if type(key)!=str:
			raise TypeError('索引必须为字符串')
		if key not in self.__fields:
			return default
		return getattr(self, key)

	def __getitem__(self, key):
		return self.get(key)
	
	def items(self):
		"""
			返回字段和字段的值的键值对
		"""
		keys = self.keys()
		return tuple((key, self.get(key)) for key in keys)

	def __iter__(self):
		"""
			返回迭代器
		"""
		self.__load_fields()
		return iter(self.__fields)


	@classmethod
	def make_page(model, filter_by=None, order_by=None, limit=20, page=1):	
		"""
			以模型DoubanMovie为例，获取满足条件的影片QuerySet
			
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
					>>> result = DoubanMovie.make_page(filter_by, order_by)

		"""

		return make_page(model, filter_by, order_by, limit, page)

	@classmethod
	def make_tree(model, filter_by=None, order_by=None, id_col='id', parentid_col='parentid', children_col='children', show_cols=None):
		if show_cols is None:
			show_cols = model().keys()

		# 获取所有数据
		data = model.make_page(filter_by=filter_by, order_by=order_by, page=None)
		return list_to_tree(data, id_col, parentid_col, children_col, show_cols)