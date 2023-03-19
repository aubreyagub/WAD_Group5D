from django import template
from restaurant.models import Menu

register = template.Library()


@register.inclusion_tag('restaurant/menus.html')
def get_menu_list():
    return {'menus': Menu.objects.all() }
