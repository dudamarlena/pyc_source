# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nodeconductor_saltstack/saltstack/migrations/0002_init_exchange_quota.py
# Compiled at: 2016-09-28 02:05:53
from __future__ import unicode_literals
from uuid import uuid4
from django.contrib.contenttypes.models import ContentType
from django.db import migrations
EXCHANGE_STORAGE_QUOTA = b'exchange_storage'
DEFAULT_EXCHANGE_STORAGE_LIMIT = 51200

def init_quotas(apps, schema_editor):
    Quota = apps.get_model(b'quotas', b'Quota')
    SaltStackServiceProjectLink = apps.get_model(b'saltstack', b'SaltStackServiceProjectLink')
    spl_ct = ContentType.objects.get_for_model(SaltStackServiceProjectLink)
    for spl in SaltStackServiceProjectLink.objects.all():
        if not Quota.objects.filter(content_type_id=spl_ct.id, object_id=spl.id, name=EXCHANGE_STORAGE_QUOTA):
            Quota.objects.create(uuid=uuid4(), name=EXCHANGE_STORAGE_QUOTA, limit=DEFAULT_EXCHANGE_STORAGE_LIMIT, usage=0, content_type_id=spl_ct.id, object_id=spl.id)


class Migration(migrations.Migration):
    dependencies = [
     ('saltstack', '0001_initial')]
    operations = [
     migrations.RunPython(init_quotas)]