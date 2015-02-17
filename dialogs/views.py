# coding=utf-8
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from dialogs.models import Dialog


class DialogView(TemplateView):
    template_name = 'dialogs/dialog.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
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

    def get_context_data(self, **kwargs):
        context = super(DialogView, self).get_context_data(**kwargs)
        context['dialogs'] = self.get_dialogs()
        return context
