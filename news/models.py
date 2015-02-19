# coding=utf-8
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _


class NewsItemManager(models.Manager):
    def for_user(self, user):
        friends_ids = list(user.friends.values_list('pk', flat=True))
        friends_ids.append(user.pk)
        return self.filter(Q(user_id__in=friends_ids) | Q(target_id__in=friends_ids))


class NewsItem(models.Model):
    TYPE_WALL_POST = 'wall_post'
    TYPE_MAKE_FRIENDS = 'make_friends'
    TYPE_BREAK_FRIENDS = 'break_friends'
    TYPE_CHOICES = (
        (TYPE_WALL_POST, _(u'сообщение на стене')),
        (TYPE_MAKE_FRIENDS, _(u'создание дружественной свзяи')),
        (TYPE_BREAK_FRIENDS, _(u'разрыв дружественной свзяи')),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='+')
    target = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='+')
    type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    content_type = models.ForeignKey(ContentType, null=True, blank=True)
    object_id = models.PositiveIntegerField(blank=True, null=True)
    news_object = GenericForeignKey()
    created = models.DateTimeField(auto_now_add=True)

    objects = NewsItemManager()

    class Meta:
        ordering = ('-created',)

    def get_template_for_display(self):
        return 'news/display_%s.html' % self.type
