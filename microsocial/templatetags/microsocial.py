# coding=utf-8
from django import template


register = template.Library()

@register.inclusion_tag('tags/form_field_errors.html')
def show_form_field_errors(field_errors, block_class=None):
    return {
        'errors': field_errors,
        'block_class': block_class
    }