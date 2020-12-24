# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/settings/migrations/0018_auto_20190429_1604.py
# Compiled at: 2019-04-29 07:35:50
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
        key = b'WALLET_CHARGING_MESSAGE'
        Setting.objects.get(key=key)
    except Exception:
        Setting.objects.create(title=b'پیام شارژ کیف پول', key=key, value=b'کیف پول شما شارژ ندارد. لطفا ابتدا کیف پول خود را شارژ بفرمایید.', value_type=b's', is_show=False, is_variable_in_home=False)


def remove_keys(apps, schema_editor):
    """
    We can't import the Post model directly as it may be a newer
    version than this migration expects. We use the historical version.
    """
    Setting = apps.get_model(b'settings', b'Setting')
    try:
        key = b'WALLET_CHARGING_MESSAGE'
        Setting.objects.get(key=key).delete()
    except Exception:
        pass


class Migration(migrations.Migration):
    dependencies = [
     ('settings', '0017_auto_20190428_0959')]
    operations = [
     migrations.RunPython(add_keys, reverse_code=remove_keys)]