from django import template
register=template.Library()
@register.filter
def logical_or(value1,value2):
   return value1 or not value2