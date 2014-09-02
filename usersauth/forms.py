#coding=utf-8
from django import forms
from users.models import User
from django.utils.translation import ugettext_lazy as _

class RegistrationForm(forms.ModelForm):

    password1 = forms.CharField(label=_(u'пароль'), min_length=6, max_length=40, widget=forms.PasswordInput)
    password2 = forms.CharField(label=_(u'повторите пароль'), min_length=6, max_length=40, widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('first_name', 'email')

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)