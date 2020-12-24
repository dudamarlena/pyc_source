# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/bouma/gitprojects/provgroningen/buildout/src/djinn_auth/djinn_auth/models/role.py
# Compiled at: 2014-12-08 06:02:47
from django.contrib.auth.models import Permission
from django.db import models
from django.utils.translation import ugettext_lazy as _

class Role(models.Model):
    """ A role is really nothing but a bundle of permissions """
    name = models.CharField(_('name'), max_length=80, unique=True)
    permissions = models.ManyToManyField(Permission, verbose_name=_('permissions'))

    class Meta:
        app_label = 'djinn_auth'
        ordering = ['name']

    def __unicode__(self):
        return self.name

    def add_permission(self, permission):
        """ Add the permission if it's not already there """
        if not self.permissions.filter(codename=permission.codename).exists():
            self.permissions.add(permission)