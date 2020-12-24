# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/packages/shops/orders/migrations/0007_auto_20190121_1856.py
# Compiled at: 2019-01-31 06:07:32
from __future__ import unicode_literals
from django.db import migrations
import uuid

def order_generate_uuid(apps, schema_editor):
    """
    We can't import the Post model directly as it may be a newer
    version than this migration expects. We use the historical version.
    """
    Object = apps.get_model(b'orders', b'Order')
    for obj in Object.objects.all():
        uu = uuid.uuid4()
        while Object.objects.filter(uuid=uu).count() > 0:
            uu = uuid.uuid4()

        obj.uuid = uu
        obj.save()


class Migration(migrations.Migration):
    dependencies = [
     ('orders', '0006_order_uuid')]
    operations = [
     migrations.RunPython(order_generate_uuid, reverse_code=migrations.RunPython.noop)]