# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/settings/migrations/0020_auto_20190623_0846.py
# Compiled at: 2020-01-05 09:49:45
# Size of source mod 2**32: 1304 bytes
from django.db import migrations

def add_keys(apps, schema_editor):
    """
    We can't import the Post model directly as it may be a newer
    version than this migration expects. We use the historical version.
    """
    Setting = apps.get_model('settings', 'Setting')
    key = ''
    try:
        key = 'USER_REGISTER_GIFT_BON_CREDITS'
        Setting.objects.get(key=key)
    except Exception:
        Setting.objects.create(title='شارژ هدیه برای ثبت نام کاربر جدید',
          key=key,
          value='0',
          value_type='i',
          is_show=False,
          is_variable_in_home=False)


def remove_keys(apps, schema_editor):
    """
    We can't import the Post model directly as it may be a newer
    version than this migration expects. We use the historical version.
    """
    Setting = apps.get_model('settings', 'Setting')
    try:
        key = 'USER_REGISTER_GIFT_BON_CREDITS'
        Setting.objects.get(key=key).delete()
    except Exception:
        pass


class Migration(migrations.Migration):
    dependencies = [
     ('settings', '0019_auto_20190525_1158')]
    operations = [
     migrations.RunPython(add_keys, reverse_code=remove_keys)]