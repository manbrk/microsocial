# coding=utf-8
from django.conf.urls import url
from users.views import UserProfileView, UserSettingsView, UserFriendsView, \
    UserIncomingView, UserOutcomingView


urlpatterns = [
    url(r'^profile/(?P<user_id>\d+)/$', UserProfileView.as_view(), name='user_profile'),
    url(r'^settings/$', UserSettingsView.as_view(), name='user_settings'),
    url(r'^friends/$', UserFriendsView.as_view(), name='user_friends'),
    url(r'^friends/incoming$', UserIncomingView.as_view(), name='user_incoming'),
    url(r'^friends/outcoming$', UserOutcomingView.as_view(), name='user_outcoming'),

]