from django import template
register = template.Library()

@register.filter
def div(value, arg):
    return int(value) / int(arg)

@register.filter
def mul(value, arg):
    return int(value) * int(arg)
