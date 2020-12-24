# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/settings/migrations/0006_auto_20181210_1432.py
# Compiled at: 2018-12-11 08:51:05
from __future__ import unicode_literals
from django.db import migrations

def command(apps, schema_editor):
    """
    We can't import the Post model directly as it may be a newer
    version than this migration expects. We use the historical version.
    """
    Product = apps.get_model(b'products', b'Product')
    Setting = apps.get_model(b'settings', b'Setting')
    key = b'PRODUCT_WALLET_ID'
    value_id = Setting.objects.get(key=key).value
    wallet = Product.objects.get(id=value_id)
    wallet.is_show_only_for_super_user = True
    wallet.save()


class Migration(migrations.Migration):
    dependencies = [
     ('settings', '0005_auto_20181130_1938')]
    operations = [
     migrations.RunPython(command, reverse_code=migrations.RunPython.noop)]