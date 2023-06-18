from django import template

register = template.Library()



@register.filter
def add_one(value):
    return value

@register.filter
def exclude_fields(value, excluded_names):
    return [field for field in value if field.name not in excluded_names]