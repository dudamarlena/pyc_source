# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nodeconductor_saltstack/exchange/migrations/0004_init_quotas.py
# Compiled at: 2016-09-28 02:05:53
from __future__ import unicode_literals
from uuid import uuid4
from django.contrib.contenttypes.models import ContentType
from django.db import models, migrations
GLOBAL_MAILBOX_SIZE_QUOTA = b'global_mailbox_size'
USER_COUNT_QUOTA = b'user_count'

def convert_mailbox_size_to_mb(apps, schema_editor):
    Tenant = apps.get_model(b'exchange', b'ExchangeTenant')
    for tenant in Tenant.objects.all():
        tenant.mailbox_size *= 1024
        tenant.save()


def init_quotas(apps, schema_editor):
    Quota = apps.get_model(b'quotas', b'Quota')
    Tenant = apps.get_model(b'exchange', b'ExchangeTenant')
    tenant_ct = ContentType.objects.get_for_model(Tenant)
    for tenant in Tenant.objects.all():
        if not Quota.objects.filter(content_type_id=tenant_ct.id, object_id=tenant.id, name=GLOBAL_MAILBOX_SIZE_QUOTA):
            Quota.objects.create(uuid=uuid4(), name=GLOBAL_MAILBOX_SIZE_QUOTA, limit=tenant.max_users * tenant.mailbox_size, usage=0, content_type_id=tenant_ct.id, object_id=tenant.id)
        if not Quota.objects.filter(content_type_id=tenant_ct.id, object_id=tenant.id, name=USER_COUNT_QUOTA):
            Quota.objects.create(uuid=uuid4(), name=USER_COUNT_QUOTA, limit=tenant.max_users, usage=0, content_type_id=tenant_ct.id, object_id=tenant.id)


class Migration(migrations.Migration):
    dependencies = [
     ('exchange', '0003_rename_tenant_model')]
    operations = [
     migrations.AlterField(model_name=b'exchangetenant', name=b'mailbox_size', field=models.PositiveSmallIntegerField(help_text=b'Maximum size of single mailbox, MB'), preserve_default=True),
     migrations.RunPython(convert_mailbox_size_to_mb),
     migrations.RunPython(init_quotas)]