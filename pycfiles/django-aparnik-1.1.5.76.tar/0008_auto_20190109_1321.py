# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/settings/migrations/0008_auto_20190109_1321.py
# Compiled at: 2019-01-10 02:09:17
from __future__ import unicode_literals
from django.db import migrations

def add_keys(apps, schema_editor):
    """
    We can't import the Post model directly as it may be a newer
    version than this migration expects. We use the historical version.
    """
    Setting = apps.get_model(b'settings', b'Setting')
    key = b''
    try:
        key = b'ORDER_CODE_PREFIX'
        Setting.objects.get(key=key)
    except Exception:
        Setting.objects.create(title=b'پیشوند کد فاکتور', key=key, value=b'APARNIK', value_type=b's', is_show=False, is_variable_in_home=False)

    try:
        key = b'POSTAL_COST'
        Setting.objects.get(key=key)
    except Exception:
        Setting.objects.create(title=b'هزینه پستی', key=key, value=0, value_type=b'i', is_show=False, is_variable_in_home=False)


class Migration(migrations.Migration):
    dependencies = [
     ('settings', '0007_auto_20190105_1314')]
    operations = [
     migrations.RunPython(add_keys, reverse_code=migrations.RunPython.noop)]