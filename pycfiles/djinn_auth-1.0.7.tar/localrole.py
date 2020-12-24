# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/bouma/gitprojects/provgroningen/buildout/src/djinn_auth/djinn_auth/models/localrole.py
# Compiled at: 2015-09-18 04:30:22
from django.db import models
from django.contrib.contenttypes.models import ContentType
from djinn_auth.models.base import RoleAssignment
try:
    from django.contrib.contenttypes.fields import GenericForeignKey
except:
    from django.contrib.contenttypes.generic import GenericForeignKey

class LocalRole(RoleAssignment):
    """ Local role for given model instance. Can be assigned either to
    user or to usergroup.
    """
    instance_ct = models.ForeignKey(ContentType, related_name='+')
    instance_id = models.PositiveIntegerField()
    instance = GenericForeignKey('instance_ct', 'instance_id')

    class Meta:
        app_label = 'djinn_auth'

    def __unicode__(self):
        return '%s is %s for %s' % (self.assignee, self.role, self.instance)