# coding=utf-8
from django.conf.urls import url
from news.views import NewsView


urlpatterns = [
    url(r'^news/$', NewsView.as_view(), name='news'),
]
