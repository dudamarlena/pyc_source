# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: C:\Users\david\Projects\cosmicdbsemantic\cosmicdb\models.py
# Compiled at: 2018-06-24 03:12:45
# Size of source mod 2**32: 1886 bytes
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.safestring import mark_safe
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from bs4 import BeautifulSoup
from sitetree.models import TreeItemBase, TreeBase

class CosmicUser(AbstractUser):
    email = models.EmailField((_('email address')), blank=True, unique=True)

    def unread_notification_no(self):
        return self.usersystemnotification_set.filter(read=False).count()

    def unread_notifications(self):
        return self.usersystemnotification_set.filter(read=False).order_by('-created_at')[:3]

    def read_notifications(self):
        return self.usersystemnotification_set.filter(read=True).order_by('-created_at')[:3]

    def read_notification_no(self):
        return self.usersystemnotification_set.filter(read=True).count()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s' % self.username


class UserSystemNotification(models.Model):
    user = models.ForeignKey((settings.AUTH_USER_MODEL), on_delete=(models.PROTECT))
    notification = models.TextField()

    def short_notification(self):
        notification_no_html = BeautifulSoup(self.notification, 'html.parser').get_text()
        return notification_no_html[:30] + '..'

    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s - %s' % (self.user, self.short_notification())


class CosmicDBTree(TreeBase):
    pass


class CosmicDBTreeItem(TreeItemBase):
    is_right = models.BooleanField(default=False)
    is_button = models.BooleanField(default=False)