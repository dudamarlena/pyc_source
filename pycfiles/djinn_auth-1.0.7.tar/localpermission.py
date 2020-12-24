# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/bouma/gitprojects/provgroningen/buildout/src/djinn_auth/djinn_auth/models/localpermission.py
# Compiled at: 2015-09-18 04:30:50
from django.db import models
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
try:
    from django.contrib.contenttypes.fields import GenericForeignKey
except:
    from django.contrib.contenttypes.generic import GenericForeignKey

class LocalPermission(models.Model):
    """Local permission for given model instance. Can be assigned either
    to user or to usergroup.

    """
    instance_ct = models.ForeignKey(ContentType, related_name='+')
    instance_id = models.PositiveIntegerField()
    instance = GenericForeignKey('instance_ct', 'instance_id')
    assignee_ct = models.ForeignKey(ContentType, related_name='+')
    assignee_id = models.PositiveIntegerField()
    assignee = GenericForeignKey('assignee_ct', 'assignee_id')
    permission = models.ForeignKey(Permission)

    class Meta:
        app_label = 'djinn_auth'

    def __unicode__(self):
        return '%s has %s for %s' % (self.assignee, self.permission,
         self.content)