#coding=utf-8
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.views import login
from django.core.signing import Signer, BadSignature
from django.core.urlresolvers import reverse_lazy
from django.http import Http404
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, RedirectView
from usersauth.forms import RegistrationForm, LoginForm, PasswordRecoveryForm
from users.models import User
from django.utils.translation import ugettext as _


def login_view(request):
    if request.user.is_authenticated():
        return redirect('main')
    return login(request, 'usersauth/user_login.html', authentication_form=LoginForm)


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
        if 'registered_user_id' in self.request.session:
            context['registered_user'] = User.objects.get(pk=self.request.session.pop('registered_user_id'))
        return context

    def post(self, request, *args, **kwargs):
        if self.form.is_valid():
            user = self.form.save()
            user.send_registration_email()
            request.session['registered_user_id'] = user.pk
            return redirect(request.path)

        return self.get(request, *args, **kwargs)


class RegistrationConfirmView(RedirectView):
    url = reverse_lazy(settings.LOGIN_URL)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            raise Http404
        try:
            user_id = Signer(salt='registration-confirm').unsign(kwargs['token'])
        except BadSignature:
            raise Http404
        user = User.objects.get(pk=user_id)
        if user.confirmed_registration:
            raise Http404
        user.confirmed_registration = True
        user.save(update_fields=('confirmed_registration',))
        messages.success(request, _(u'Регистрация успешна.'))
        return super(RegistrationConfirmView, self).dispatch(request, *args, **kwargs)


class PasswordRecoveryView(TemplateView):
    template_name = 'usersauth/user_password_recover.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return redirect('main')
        self.form = PasswordRecoveryForm(request.POST or None)
        return super(PasswordRecoveryView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(PasswordRecoveryView, self).get_context_data(**kwargs)
        context['form'] = self.form
        if 'password_recovery_user_id' in self.request.session
            context['password_recovery_user'] = User.objects.get(pk=self.request.session.pop('password_recovery_user_id'))
        return context

    def post(self, request, *args, **kwargs):
        if self.form.is_valid():
            user = self.form.get_user()
            #todo отправить емаил
            request.session['password_recovery_user_id'] = user.pk
            return redirect(request.path)
        return self.get(request, *args, **kwargs)

class PasswordRecoveryConfirmView(TemplateView):
    template_name = 'usersauth/user_password_recovery_form.html'