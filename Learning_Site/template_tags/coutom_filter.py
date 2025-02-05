from django import template

register = template.Library()

@register.filter
def chunk(queryset, chunk_size):
    """Chunks the queryset into groups of the specified size."""
    return [queryset[i:i + chunk_size] for i in range(0, len(queryset), chunk_size)]

