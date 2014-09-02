#coding=utf-8
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from usersauth.forms import RegistrationForm
from users.models import User


def login_view(request):
    return render(request, 'usersauth/user_login.html')


class RegistrationView(TemplateView):
    template_name = 'usersauth/user_registration.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return redirect('main')
        self.form = RegistrationForm(request.POST or None)
        return super(RegistrationView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(RegistrationView, self).get_context_data(**kwargs)
        context['form'] = self.form
        return context

    def post(self, request, *args, **kwargs):
        if self.form.is_valid():
            user = self.form.save()
            request.session['registered_user_id'] = user.pk
            return redirect(request.path)

        return self.get(request, *args, **kwargs)


class PasswordRecoveryView(TemplateView):
    template_name = 'usersauth/user_password_recover.html'