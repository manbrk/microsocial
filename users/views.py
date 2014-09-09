#coding=utf-8
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView
from users.models import User


class UserProfileView(TemplateView):
    template_name = 'users/user_profile.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated() and int(kwargs['user_id']) == request.user.pk:
            self.user = request.user
        else:
            self.user = get_object_or_404(User, pk=kwargs['user_id'])
        return super(UserProfileView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(UserProfileView, self).get_context_data(**kwargs)
        context['profile_user'] = self.user
        return context