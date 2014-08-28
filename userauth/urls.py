from django.conf.urls import patterns, url, include

urlpatterns = patterns('',
    url(r'^user/', include('django.contrib.flatpages.urls')),
)