# coding=utf-8
from django.conf import settings
from django.db import models
from django.db.models import Q


class DialogManager(models.Manager):
    def for_user(self, user):
        return self.filter(Q(user1=user) | Q(user2=user))

    def get_or_create(self, sender, recipient):
        if sender == recipient:
            return
        try:
            return self.get(Q(user1=sender, user2=recipient) | Q(user1=recipient, user2=sender))
        except Dialog.DoesNotExist:
            return self.create(user1=sender, user2=recipient)


class Dialog(models.Model):
    user1 = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='+')
    user2 = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='+')
    last_message = models.ForeignKey('Message', related_name='+', null=True, blank=True)

    objects = DialogManager()

    class Meta:
        unique_together = ('user1', 'user2')

    def __unicode__(self):
        return u'Dialog #%s #%s' % (self.user1_id, self.user2_id)

    def get_opponent(self, user):
        return self.user2 if self.user1 == user else self.user1

class Message(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='+')
    dialog = models.ForeignKey(Dialog, related_name='messages')
    text = models.TextField(max_length=2000)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering =('-created',)

    def __unicode__(self):
        return u'Message #%s' % self.pk