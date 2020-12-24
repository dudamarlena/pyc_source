# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/settings/migrations/0011_auto_20190122_2122.py
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
        key = b'MOHR_ICON'
        Setting.objects.get(key=key)
    except Exception:
        Setting.objects.create(title=b'آیکن مهر', key=key, value=b'', value_type=b's', is_show=False, is_variable_in_home=False)

    try:
        key = b'PROJECT_NAME'
        Setting.objects.get(key=key)
    except Exception:
        Setting.objects.create(title=b'نام پروژه', key=key, value=b'آپارنیک', value_type=b's', is_show=False, is_variable_in_home=False)

    try:
        key = b'ECONOMICAL_NUMBER'
        Setting.objects.get(key=key)
    except Exception:
        Setting.objects.create(title=b'کد اقتصادی', key=key, value=b'', value_type=b's', is_show=False, is_variable_in_home=False)

    try:
        key = b'REGISTRATION_NUMBER'
        Setting.objects.get(key=key)
    except Exception:
        Setting.objects.create(title=b'شماره ثبت', key=key, value=b'', value_type=b's', is_show=False, is_variable_in_home=False)

    try:
        key = b'POSTAL_CODE'
        Setting.objects.get(key=key)
    except Exception:
        Setting.objects.create(title=b'کد پستی', key=key, value=b'', value_type=b's', is_show=False, is_variable_in_home=False)

    try:
        key = b'PROJECT_CITY_ID'
        Setting.objects.get(key=key)
    except Exception:
        Setting.objects.create(title=b'آی دی شهر پروژه', key=key, value=b'1', value_type=b'i', is_show=False, is_variable_in_home=False)

    try:
        key = b'ADDRESS'
        Setting.objects.get(key=key)
    except Exception:
        Setting.objects.create(title=b'آدرس', key=key, value=b'', value_type=b's', is_show=False, is_variable_in_home=False)

    try:
        key = b'PHONE'
        Setting.objects.get(key=key)
    except Exception:
        Setting.objects.create(title=b'تلفن', key=key, value=b'', value_type=b's', is_show=False, is_variable_in_home=False)


class Migration(migrations.Migration):
    dependencies = [
     ('settings', '0010_auto_20190117_1849')]
    operations = [
     migrations.RunPython(add_keys, reverse_code=migrations.RunPython.noop)]