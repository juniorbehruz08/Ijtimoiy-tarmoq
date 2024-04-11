from django import template
from ..models import Category

register = template.Library()


@register.simple_tag()
def sort():
    sort = {
        '-created_date': 'Last',
        'created_date': 'Old',
        '-views': 'Most',
        'views': 'Less',

    }
    return sort


@register.simple_tag()
def get_categories():
    return Category.objects.all()
