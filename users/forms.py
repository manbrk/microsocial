# coding=utf-8
from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.utils.translation import ugettext
from users.models import User, UserWallPost
from django.utils.translation import ugettext_lazy as _

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('avatar', 'first_name', 'last_name', 'sex', 'birth_date', 'city', 'job', 'about_me', 'interests')

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields['birth_date'].widget.attrs['placeholder'] = ugettext(u'Введите дату в формате гггг-мм-дд')


class UserPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super(UserPasswordChangeForm, self).__init__(*args, **kwargs)
        for field_name in ('old_password', 'new_password1', 'new_password2'):
            self.fields[field_name] = self.fields.pop(field_name)


class UserEmailChangeForm(forms.Form):
    new_email = forms.EmailField(max_length=75, label=_(u'новый email'))
    password = forms.CharField(label=_(u'текущий пароль'), widget=forms.PasswordInput)

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(UserEmailChangeForm, self).__init__(*args, **kwargs)


    def clean_new_email(self):
        new_email = self.cleaned_data['new_email'].strip()
        if User.objects.filter(email=new_email).exclude(pk=self.user.pk).exists:
            raise forms.ValidationError(ugettext(u'Пользователь с таким email уже существует.'))
        return new_email

    def clean_password(self):
        password = self.cleaned_data['password']
        if not self.user.check_password(password):
            raise forms.ValidationError(ugettext(u'Введен неправильный пароль.'))
        return password

    def save(self, commit=True):
        self.user.email = self.cleaned_data['new_email']
        if commit:
            self.user.save()
        return self.user

class UserWallPostForm(forms.ModelForm):
    class Meta:
        model = UserWallPost
        fields = ('content',)
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4, 'placeholder': _(u'напишите на стене...')})
        }

    def __init__(self, *args, **kwargs):
        super(UserWallPostForm, self).__init__(*args, **kwargs)

    def clean_content(self):
        return self.cleaned_data['content'].strip()

class SearchForm(forms.Form):
    name = forms.CharField(label=_(u'имя, фамилия'), required=False)
    sex = forms.TypedChoiceField(label=_(u'пол'), required=False, choices=((0, _(u'все')), ) + User.SEX_CHOICES[1:], coerce=lambda val: int(val))
    by_from = forms.IntegerField(label=_(u'год рождения от'), required=False, widget=forms.NumberInput(attrs={'placeholder': _(u'от')}))
    by_to = forms.IntegerField(label=_(u'год рождения до'), required=False, widget=forms.NumberInput(attrs={'placeholder': _(u'до')}))
    city = forms.CharField(label=_(u'город'), required=False)
    job = forms.CharField(label=_(u'место работы'), required=False)
    about_me = forms.CharField(label=_(u'о себе'), required=False)
    interests = forms.CharField(label=_(u'интересы'), required=False)

    def get_values_list(self, field_name):
        val = self.cleaned_data.get(field_name)
        if isinstance(val, basestring):
            val = val.strip().split()
        return val or []
