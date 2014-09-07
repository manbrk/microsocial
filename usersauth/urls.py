# coding=utf-8
from django.conf import settings
from django.conf.urls import patterns, url
from django.contrib.auth.views import logout
from usersauth.views import RegistrationView, RegistrationConfirmView, PasswordRecoveryView, \
    PasswordRecoveryConfirmView


urlpatterns = patterns('',
    url(r'^login/$', 'usersauth.views.login_view', name='login'),
    url(r'^logout/$', logout, {'next_page': settings.LOGIN_URL}, name='logout'),
    url(r'^registration/$', RegistrationView.as_view(), name='registration'),
    url(r'^registration/(?P<token>.+)/$', RegistrationConfirmView.as_view(), name='registration_confirm'),
    url(r'^password-recovery/$', PasswordRecoveryView.as_view(), name='password_recovery'),
    url(r'^password-recovery/(?P<token>.+)/$', PasswordRecoveryConfirmView.as_view(), name='password_recovery'),
)