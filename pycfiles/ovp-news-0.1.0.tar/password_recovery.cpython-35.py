# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/arroyo/ovp/suzano-ovp/django-ovp-users/ovp_users/models/password_recovery.py
# Compiled at: 2017-02-22 18:06:29
# Size of source mod 2**32: 722 bytes
import uuid
from django.db import models
from django.utils.translation import ugettext_lazy as _

class PasswordRecoveryToken(models.Model):
    user = models.ForeignKey('User', blank=True, null=True)
    token = models.CharField(_('Token'), max_length=128, null=False, blank=False)
    created_date = models.DateTimeField(_('Created date'), auto_now_add=True, blank=True, null=True)
    used_date = models.DateTimeField(_('Used date'), default=None, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.token = uuid.uuid4()
            self.user.mailing().sendRecoveryToken({'token': self})
        super(PasswordRecoveryToken, self).save(*args, **kwargs)

    class Meta:
        app_label = 'ovp_users'