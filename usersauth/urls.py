# coding=utf-8
from django.conf.urls import patterns, url
from usersauth.views import RegistrationView, RegistrationConfirmView, PasswordRecoveryView


urlpatterns = patterns('',
    url(r'^login/$', 'usersauth.views.login_view', name='login'),
    url(r'^registration/$', RegistrationView.as_view(), name='registration'),
    url(r'^registration/(?P<token>.+)/$', RegistrationConfirmView.as_view(), name='registration_confirm'),
    url(r'^password-recovery/$', PasswordRecoveryView.as_view(), name='password_recovery'),
)