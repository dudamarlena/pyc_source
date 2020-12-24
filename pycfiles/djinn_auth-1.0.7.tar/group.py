# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/bouma/gitprojects/provgroningen/buildout/src/djinn_auth/djinn_auth/models/group.py
# Compiled at: 2016-06-28 16:31:04
from django.db import models
from django.conf import settings
from django.contrib.auth.models import Permission
from polymorphic.models import PolymorphicModel

class Group(PolymorphicModel):
    """Abstract group base. The polymorphism enables you to extend this
    class in several ways, but find all kinds with the Group.objects
    manager

    """
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)
    permissions = models.ManyToManyField(Permission, related_name='groups', blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = [
         'name']
        app_label = 'djinn_auth'