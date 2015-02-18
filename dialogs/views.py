# coding=utf-8
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from dialogs.forms import MessageForm
from dialogs.models import Dialog


class DialogView(TemplateView):
    template_name = 'dialogs/dialog.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.opponnent = None
        self.dialog = None
        self.form = None
        if 'user_id' in kwargs:
            self.opponnent = get_object_or_404(get_user_model(), pk=kwargs['user_id'])
            self.dialog = Dialog.objects.get_or_create(request.user, self.opponnent)
            if not self.dialog:
                raise Http404
            self.form = MessageForm(request.POST or None)
        return super(DialogView, self).dispatch(request, *args, **kwargs)

    def get_dialogs(self):
        qs = Dialog.objects.for_user(self.request.user).select_related('user1', 'user2').filter(
            last_message__isnull=False
        ).order_by('-last_message__created')
        paginator = Paginator(qs, 20)
        page = self.request.GET.get('dialogs_page')
        try:
            items = paginator.page(page)
        except PageNotAnInteger:
            items = paginator.page(1)
        except EmptyPage:
            items = paginator.page(paginator.num_pages)
        return items

    def get_messages(self):
        if not self.dialog:
            return
        paginator = Paginator(self.dialog.messages.all(), 20)
        page = self.request.GET.get('messages_page')
        try:
            items = paginator.page(page)
        except PageNotAnInteger:
            items = paginator.page(1)
        except EmptyPage:
            items = paginator.page(paginator.num_pages)
        return items

    def get_context_data(self, **kwargs):
        context = super(DialogView, self).get_context_data(**kwargs)
        context['dialogs'] = self.get_dialogs()
        context['opponent'] = self.opponnent
        context['dialog_messages'] = self.get_messages()
        context['form'] = self.form
        return context

    def post(self, request, *args, **kwargs):
        if self.form and self.form.is_valid():
            message = self.form.save(commit=False)
            message.sender = request.user
            message.dialog = self.dialog
            message.save()
            return redirect(request.get_full_path())
        return self.get(request, *args, **kwargs)