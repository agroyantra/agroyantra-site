from django import template
register = template.Library()

@register.filter
def split_colon_key(value):
    """Returns part before first colon"""
    return value.split(':', 1)[0].strip()

@register.filter
def split_colon_val(value):
    """Returns part after first colon"""
    parts = value.split(':', 1)
    return parts[1].strip() if len(parts) > 1 else ''
