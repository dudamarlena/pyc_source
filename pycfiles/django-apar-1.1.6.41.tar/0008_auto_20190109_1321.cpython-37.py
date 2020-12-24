# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/settings/migrations/0008_auto_20190109_1321.py
# Compiled at: 2020-01-05 09:49:45
# Size of source mod 2**32: 1243 bytes
from django.db import migrations

def add_keys(apps, schema_editor):
    """
    We can't import the Post model directly as it may be a newer
    version than this migration expects. We use the historical version.
    """
    Setting = apps.get_model('settings', 'Setting')
    key = ''
    try:
        key = 'ORDER_CODE_PREFIX'
        Setting.objects.get(key=key)
    except Exception:
        Setting.objects.create(title='پیشوند کد فاکتور',
          key=key,
          value='APARNIK',
          value_type='s',
          is_show=False,
          is_variable_in_home=False)

    try:
        key = 'POSTAL_COST'
        Setting.objects.get(key=key)
    except Exception:
        Setting.objects.create(title='هزینه پستی',
          key=key,
          value=0,
          value_type='i',
          is_show=False,
          is_variable_in_home=False)


class Migration(migrations.Migration):
    dependencies = [
     ('settings', '0007_auto_20190105_1314')]
    operations = [
     migrations.RunPython(add_keys, reverse_code=(migrations.RunPython.noop))]