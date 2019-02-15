from django import template

register = template.Library()

from blog.models import CATEGORIES


@register.inclusion_tag('blog/templatetags/cat_list.html')
def cat_list():
    return {'categories':CATEGORIES.list}
