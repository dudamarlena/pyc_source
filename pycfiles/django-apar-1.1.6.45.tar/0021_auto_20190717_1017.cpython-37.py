# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/settings/migrations/0021_auto_20190717_1017.py
# Compiled at: 2020-01-05 09:49:45
# Size of source mod 2**32: 3449 bytes
from django.db import migrations

def add_keys(apps, schema_editor):
    """
    We can't import the Post model directly as it may be a newer
    version than this migration expects. We use the historical version.
    """
    Setting = apps.get_model('settings', 'Setting')
    key = ''
    try:
        key = 'PROJECT_DESCRIPTION'
        Setting.objects.get(key=key)
    except Exception:
        Setting.objects.create(title='توضیحات پروژه',
          key=key,
          value='',
          value_type='s',
          is_show=False,
          is_variable_in_home=False)

    try:
        key = 'APPSTORE_LINK'
        Setting.objects.get(key=key)
    except Exception:
        Setting.objects.create(title='لینک اپ استور',
          key=key,
          value='',
          value_type='s',
          is_show=False,
          is_variable_in_home=False)

    try:
        key = 'IOS_LINK'
        Setting.objects.get(key=key)
    except Exception:
        Setting.objects.create(title='لینک iOS',
          key=key,
          value='',
          value_type='s',
          is_show=False,
          is_variable_in_home=False)

    try:
        key = 'GOOGLE_PLAY_LINK'
        Setting.objects.get(key=key)
    except Exception:
        Setting.objects.create(title='لینک گوگل پلی',
          key=key,
          value='',
          value_type='s',
          is_show=False,
          is_variable_in_home=False)

    try:
        key = 'ANDROID_LINK'
        Setting.objects.get(key=key)
    except Exception:
        Setting.objects.create(title='لینک APK',
          key=key,
          value='',
          value_type='s',
          is_show=False,
          is_variable_in_home=False)

    try:
        key = 'APPLICATION_IMAGE'
        Setting.objects.get(key=key)
    except Exception:
        Setting.objects.create(title='عکس نرم افزار',
          key=key,
          value='',
          value_type='s',
          is_show=False,
          is_variable_in_home=False)


def remove_keys(apps, schema_editor):
    """
    We can't import the Post model directly as it may be a newer
    version than this migration expects. We use the historical version.
    """
    Setting = apps.get_model('settings', 'Setting')
    try:
        key = 'PROJECT_DESCRIPTION'
        Setting.objects.get(key=key).delete()
    except Exception:
        pass

    try:
        key = 'APPSTORE_LINK'
        Setting.objects.get(key=key).delete()
    except Exception:
        pass

    try:
        key = 'IOS_LINK'
        Setting.objects.get(key=key).delete()
    except Exception:
        pass

    try:
        key = 'GOOGLE_PLAY_LINK'
        Setting.objects.get(key=key).delete()
    except Exception:
        pass

    try:
        key = 'ANDROID_LINK'
        Setting.objects.get(key=key).delete()
    except Exception:
        pass

    try:
        key = 'APPLICATION_IMAGE'
        Setting.objects.get(key=key).delete()
    except Exception:
        pass


class Migration(migrations.Migration):
    dependencies = [
     ('settings', '0020_auto_20190623_0846')]
    operations = [
     migrations.RunPython(add_keys, reverse_code=remove_keys)]