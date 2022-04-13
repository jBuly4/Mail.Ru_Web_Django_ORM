from django import template

register = template.Library()


@register.filter(name='inc')
def summ(a, b):
    try:
        res = int(a) + int(b)
        return res
    except:
        return ''


@register.simple_tag(name='division')
def divide(a, b, to_int=False):
    try:
        a = int(a)
        b = int(b)
        if to_int:
            return int(a / b)
        else:
            return a / b
    except:
        return ''

