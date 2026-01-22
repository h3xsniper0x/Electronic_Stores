from django import template
from products.models import Category

register = template.Library()

@register.simple_tag
def get_categories():
    """Returns all categories for usage in templates."""
    return Category.objects.all()
