from django.db import models
from django.utils.translation import ugettext_lazy as _

from utils.make_query import make_page
from utils.base_model import BaseModel

# Create your models here.
class Navigation(models.Model, BaseModel):

	id = models.CharField(_('主键ID'), max_length=32, primary_key=True, blank=False, default='')
	name = models.CharField(_('栏目名称'), max_length=100,  blank=False)
	parentid = models.CharField(_('父栏目ID'), max_length=32,  blank=True)
	ismenu = models.BooleanField(_('是否为菜单（栏目将显示在网站导航条中)'), blank=False)
	level = models.PositiveSmallIntegerField(_('层级'), blank=False)
	order = models.PositiveSmallIntegerField(_('层级内的顺序（正序）'), blank=False)
	url = models.CharField(_('栏目的url（注意该url为app:name格式，如user:login）'), max_length=100, blank=True)

	class Meta:
		db_table = 't_navigation'
