#coding=utf-8
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from usersauth.forms import RegistrationForm


def login_view(request):
    return render(request, 'usersauth/user_login.html')


class RegistrationView(TemplateView):
    template_name = 'usersauth/user_registration.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return redirect('main')
        self.form = RegistrationForm(request.POST or None)
        return super(RegistrationView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        context = super(RegistrationView).get_context_data(**kwargs)
        context['form'] = self.form
        return context

class PasswordRecoveryView(TemplateView):
    template_name = 'usersauth/user_password_recover.html'