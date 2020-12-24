# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/settings/migrations/0009_auto_20190115_2118.py
# Compiled at: 2019-01-31 06:07:32
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
        key = b'ZARINPAL_MERCHENT_CODE'
        Setting.objects.get(key=key)
    except Exception:
        Setting.objects.create(title=b'مرچنت کد زرین پال', key=key, value=b'', value_type=b's', is_show=False, is_variable_in_home=False)


class Migration(migrations.Migration):
    dependencies = [
     ('settings', '0008_auto_20190109_1321')]
    operations = [
     migrations.RunPython(add_keys, reverse_code=migrations.RunPython.noop)]