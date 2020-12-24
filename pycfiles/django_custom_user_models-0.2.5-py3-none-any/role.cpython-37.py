# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: M:\Programming\Project\django-auth\auth\CustomAuth\models\role.py
# Compiled at: 2019-12-11 08:36:50
# Size of source mod 2**32: 660 bytes
from django.db import models
import django.utils.translation as _
from django.contrib.auth.models import Permission

class Role(models.Model):
    name = models.CharField((_('name of role')),
      max_length=250)
    permissions = models.ManyToManyField(Permission,
      verbose_name=(_('Role Permission')),
      related_name='roles',
      related_query_name='role',
      blank=True,
      null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('role')
        verbose_name_plural = _('roles')
        ordering = ('name', )