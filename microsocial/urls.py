from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.decorators.csrf import csrf_exempt
from django.views.i18n import set_language

urlpatterns = patterns('',
    url(r'^$', 'microsocial.views.main', name='main'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^i18n/setlang/$', csrf_exempt(set_language), name='set_language'),
    url(r'', include('users.urls')),
    url(r'', include('django.contrib.flatpages.urls')),
)
