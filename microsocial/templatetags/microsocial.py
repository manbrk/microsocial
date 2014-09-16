# coding=utf-8
from django import template


register = template.Library()

@register.inclusion_tag('tags/form_field_errors.html')
def show_form_field_errors(field_errors, block_class=None):
    return {
        'errors': field_errors,
        'block_class': block_class
    }

@register.inclusion_tag('tags/form_field_errors.html')
def show_form_errors(form, block_class=None):
    return {
        'errors': form.errors.get('__all__'),
        'block_class': block_class,
    }

@register.inclusion_tag('tags/messages.html', takes_context=True)
def show_messages(context, show=True):
    return {'messages': (context.get('messages') if show else None)}

@register.inclusion_tag('tags/paginator.html')
def show_paginator(page, page_arg_name='page'):
    return {
        'page': page,
        'page_arg_name': page_arg_name,
    }