#coding=utf-8
from django.contrib import admin
from users.models import User, UserWallPost, FriendInvitation


admin.site.register(User)
admin.site.register(FriendInvitation)
admin.site.register(UserWallPost)