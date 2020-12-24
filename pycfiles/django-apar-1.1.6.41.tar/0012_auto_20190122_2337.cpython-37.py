# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/settings/migrations/0012_auto_20190122_2337.py
# Compiled at: 2020-01-05 09:49:45
# Size of source mod 2**32: 986 bytes
from django.db import migrations

def add_keys(apps, schema_editor):
    """
    We can't import the Post model directly as it may be a newer
    version than this migration expects. We use the historical version.
    """
    Setting = apps.get_model('settings', 'Setting')
    key = ''
    try:
        key = 'INVITATION_FORMAT_STRING'
        Setting.objects.get(key=key)
    except Exception:
        Setting.objects.create(title=' کد دعوت',
          key=key,
          value='شما می توانید با کد {{}} به برنامه بپیوندید.',
          value_type='s',
          is_show=False,
          is_variable_in_home=True)


class Migration(migrations.Migration):
    dependencies = [
     ('settings', '0011_auto_20190122_2122')]
    operations = [
     migrations.RunPython(add_keys, reverse_code=(migrations.RunPython.noop))]