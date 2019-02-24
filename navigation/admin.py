from django.contrib import admin
from navigation.models import Navigation

class NavigationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'parentid', 'ismenu', 'level', 'order', 'url')
    search_fields = ('name', 'parentid', 'level')
    ordering = ('level', 'parentid', 'order')


# Register your models here.
admin.site.register(Navigation, NavigationAdmin)