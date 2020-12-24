# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/settings/migrations/0007_auto_20190105_1314.py
# Compiled at: 2020-01-05 09:49:45
# Size of source mod 2**32: 950 bytes
from django.db import migrations

def add_keys(apps, schema_editor):
    """
    We can't import the Post model directly as it may be a newer
    version than this migration expects. We use the historical version.
    """
    Setting = apps.get_model('settings', 'Setting')
    key = ''
    try:
        key = 'COURSE_IGNORE_IN_LIST_IDS'
        Setting.objects.get(key=key)
    except Exception:
        Setting.objects.create(title='دوره هایی که در لیست نمی آیند',
          key=key,
          value='',
          value_type='s',
          is_show=False,
          is_variable_in_home=True)


class Migration(migrations.Migration):
    dependencies = [
     ('settings', '0006_auto_20181210_1432')]
    operations = [
     migrations.RunPython(add_keys, reverse_code=(migrations.RunPython.noop))]