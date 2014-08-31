#coding=utf-8
from django.shortcuts import render
from django.views.generic import TemplateView


class UserProfileView(TemplateView):
    template_name = 'users/user_profile.html'