# coding=utf-8
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView


class DialogView(TemplateView):
    template_name = 'dialogs/dialog.html'


    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(DialogView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(DialogView, self).get_context_data(**kwargs)
        return context
