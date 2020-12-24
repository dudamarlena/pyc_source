# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/settings/migrations/0011_auto_20190122_2122.py
# Compiled at: 2020-01-05 09:49:45
# Size of source mod 2**32: 3117 bytes
from django.db import migrations

def add_keys(apps, schema_editor):
    """
    We can't import the Post model directly as it may be a newer
    version than this migration expects. We use the historical version.
    """
    Setting = apps.get_model('settings', 'Setting')
    key = ''
    try:
        key = 'MOHR_ICON'
        Setting.objects.get(key=key)
    except Exception:
        Setting.objects.create(title='آیکن مهر',
          key=key,
          value='',
          value_type='s',
          is_show=False,
          is_variable_in_home=False)

    try:
        key = 'PROJECT_NAME'
        Setting.objects.get(key=key)
    except Exception:
        Setting.objects.create(title='نام پروژه',
          key=key,
          value='آپارنیک',
          value_type='s',
          is_show=False,
          is_variable_in_home=False)

    try:
        key = 'ECONOMICAL_NUMBER'
        Setting.objects.get(key=key)
    except Exception:
        Setting.objects.create(title='کد اقتصادی',
          key=key,
          value='',
          value_type='s',
          is_show=False,
          is_variable_in_home=False)

    try:
        key = 'REGISTRATION_NUMBER'
        Setting.objects.get(key=key)
    except Exception:
        Setting.objects.create(title='شماره ثبت',
          key=key,
          value='',
          value_type='s',
          is_show=False,
          is_variable_in_home=False)

    try:
        key = 'POSTAL_CODE'
        Setting.objects.get(key=key)
    except Exception:
        Setting.objects.create(title='کد پستی',
          key=key,
          value='',
          value_type='s',
          is_show=False,
          is_variable_in_home=False)

    try:
        key = 'PROJECT_CITY_ID'
        Setting.objects.get(key=key)
    except Exception:
        Setting.objects.create(title='آی دی شهر پروژه',
          key=key,
          value='1',
          value_type='i',
          is_show=False,
          is_variable_in_home=False)

    try:
        key = 'ADDRESS'
        Setting.objects.get(key=key)
    except Exception:
        Setting.objects.create(title='آدرس',
          key=key,
          value='',
          value_type='s',
          is_show=False,
          is_variable_in_home=False)

    try:
        key = 'PHONE'
        Setting.objects.get(key=key)
    except Exception:
        Setting.objects.create(title='تلفن',
          key=key,
          value='',
          value_type='s',
          is_show=False,
          is_variable_in_home=False)


class Migration(migrations.Migration):
    dependencies = [
     ('settings', '0010_auto_20190117_1849')]
    operations = [
     migrations.RunPython(add_keys, reverse_code=(migrations.RunPython.noop))]