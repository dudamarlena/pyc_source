# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/rowan/Nyaruka/dash/dash_test_runner/testapp/models.py
# Compiled at: 2018-08-14 12:18:01
# Size of source mod 2**32: 1276 bytes
from django_redis import get_redis_connection
from django.db import models
import django.utils.translation as _
from dash.orgs.models import Org, OrgBackend
from dash.utils.sync import BaseSyncer

class Contact(models.Model):
    org = models.ForeignKey(Org, on_delete=(models.PROTECT))
    uuid = models.CharField(max_length=36, unique=True)
    name = models.CharField(verbose_name=(_('Name')), max_length=128)
    is_active = models.BooleanField(default=True)
    backend = models.ForeignKey(OrgBackend, on_delete=(models.PROTECT))

    @classmethod
    def lock(cls, org, uuid):
        return get_redis_connection().lock(('contact-lock:%d:%s' % (org.pk, uuid)), timeout=60)


class ContactSyncer(BaseSyncer):
    model = Contact
    local_backend_attr = 'backend'

    def local_kwargs(self, org, remote):
        if remote.blocked:
            return
        return {'org': org, 
         'uuid': remote.uuid, 
         'name': remote.name, 
         self.local_backend_attr: self.backend}

    def update_required(self, local, remote, remote_as_kwargs):
        return local.name != remote.name


class APIBackend(object):

    def __init__(self, backend):
        self.backend = backend