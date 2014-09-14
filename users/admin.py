#coding=utf-8
from django.contrib import admin
from users.models import User, UserWallPost


admin.site.register(User)
admin.site.register(UserWallPost)