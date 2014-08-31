#coding=utf-8
from django.shortcuts import render
from django.views.generic import TemplateView


def login_view(request):
    return render(request, 'usersauth/user_login.html')


class RegistrationView(TemplateView):
    template_name = 'usersauth/user_registration.html'

class PasswordRecoveryView(TemplateView):
    template_name = 'usersauth/user_password_recover.html'