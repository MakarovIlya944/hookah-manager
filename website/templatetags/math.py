from django import template

register = template.Library()

@register.filter(is_safe=True)
def mult(value, arg): # Only one argument.
    """Mult by value"""
    try:
        a = int(value)
        b = int(arg)
        return str(a * b)
    except Exception :
        return ''