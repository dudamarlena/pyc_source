# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/bouma/gitprojects/provgroningen/buildout/src/djinn_auth/djinn_auth/models/base.py
# Compiled at: 2015-09-18 04:30:08
from django.db import models
from django.contrib.contenttypes.models import ContentType
from djinn_auth.models.role import Role
try:
    from django.contrib.contenttypes.fields import GenericForeignKey
except:
    from django.contrib.contenttypes.generic import GenericForeignKey

class RoleAssignment(models.Model):
    """Abstract role assignment class"""
    assignee_ct = models.ForeignKey(ContentType, related_name='+')
    assignee_id = models.PositiveIntegerField()
    assignee = GenericForeignKey('assignee_ct', 'assignee_id')
    role = models.ForeignKey(Role)

    class Meta:
        app_label = 'djinn_auth'
        abstract = True

    def __unicode__(self):
        return '%s is %s' % (self.assignee, self.role)