# coding=utf-8
from django import template
from django.conf import settings


register = template.Library()

@register.filter
def get_avatar(user):
    try:
        return user.avatar.url
    except ValueError:
        return '%susers/img/poker_face_avatar.png' % settings.STATIC_URL
