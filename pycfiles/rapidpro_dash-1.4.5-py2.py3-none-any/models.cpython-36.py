# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/rowan/Nyaruka/dash/dash_test_runner/testapp/models.py
# Compiled at: 2017-04-17 16:26:07
# Size of source mod 2**32: 1029 bytes
from __future__ import unicode_literals
from dash.orgs.models import Org
from dash.utils.sync import BaseSyncer
from django.db import models
from django.utils.translation import ugettext as _
from django_redis import get_redis_connection

class Contact(models.Model):
    org = models.ForeignKey(Org)
    uuid = models.CharField(max_length=36, unique=True)
    name = models.CharField(verbose_name=(_('Name')), max_length=128)
    is_active = models.BooleanField(default=True)

    @classmethod
    def lock(cls, org, uuid):
        return get_redis_connection().lock(('contact-lock:%d:%s' % (org.pk, uuid)), timeout=60)


class ContactSyncer(BaseSyncer):
    model = Contact

    def local_kwargs(self, org, remote):
        if remote.blocked:
            return
        else:
            return {'org':org, 
             'uuid':remote.uuid, 
             'name':remote.name}

    def update_required(self, local, remote, remote_as_kwargs):
        return local.name != remote.name