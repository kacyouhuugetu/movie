from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
@stringfilter
def split(value, arg):
	return value.split(arg)

@register.filter
@stringfilter
def replace(value, arg):
	old, *new = arg.split(',', 1)
	new = '' if len(new)==0 else new[0]

	return value.replace(old, new)

