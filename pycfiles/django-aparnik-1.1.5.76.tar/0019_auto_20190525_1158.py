# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/settings/migrations/0019_auto_20190525_1158.py
# Compiled at: 2019-05-25 04:20:17
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
        key = b'APPROVE_REVIEW'
        Setting.objects.get(key=key)
    except Exception:
        Setting.objects.create(title=b'منتشر شدن پیام ها به صورت پیش فرض', key=key, value=b'False', value_type=b'b', is_show=False, is_variable_in_home=False)

    try:
        key = b'USER_DEFAULT_LIMIT_DEVICE_LOGIN'
        Setting.objects.get(key=key)
    except Exception:
        Setting.objects.create(title=b'تعداد گوشی های مجاز هر کاربر', key=key, value=b'1', value_type=b'i', is_show=False, is_variable_in_home=False)

    try:
        key = b'USER_IS_LIMIT_DEVICE_LOGIN_ACTIVE'
        Setting.objects.get(key=key)
    except Exception:
        Setting.objects.create(title=b'فعال بودن محدودیت دستگاه', key=key, value=b'False', value_type=b'b', is_show=False, is_variable_in_home=False)

    try:
        key = b'MAX_PRODUCT_SHARING_USER_ALLOWED_PER_PRODUCT'
        Setting.objects.get(key=key)
    except Exception:
        Setting.objects.create(title=b'تعداد دسترسی های داده شده توسط این کاربر برای یک کالای خاص', key=key, value=b'1', value_type=b'i', is_show=False, is_variable_in_home=False)

    try:
        key = b'MAX_PRODUCT_SHARING_USER_ALLOWED_FOR_ALL_PRODUCTS'
        Setting.objects.get(key=key)
    except Exception:
        Setting.objects.create(title=b'تعداد دسترسی های داده شده توسط این کاربر برای همه کالاها', key=key, value=b'10', value_type=b'i', is_show=False, is_variable_in_home=False)


def remove_keys(apps, schema_editor):
    """
    We can't import the Post model directly as it may be a newer
    version than this migration expects. We use the historical version.
    """
    Setting = apps.get_model(b'settings', b'Setting')
    try:
        key = b'APPROVE_REVIEW'
        Setting.objects.get(key=key).delete()
    except Exception:
        pass

    try:
        key = b'USER_DEFAULT_LIMIT_DEVICE_LOGIN'
        Setting.objects.get(key=key).delete()
    except Exception:
        pass

    try:
        key = b'USER_IS_LIMIT_DEVICE_LOGIN_ACTIVE'
        Setting.objects.get(key=key).delete()
    except Exception:
        pass

    try:
        key = b'MAX_PRODUCT_SHARING_USER_ALLOWED_PER_PRODUCT'
        Setting.objects.get(key=key).delete()
    except Exception:
        pass

    try:
        key = b'MAX_PRODUCT_SHARING_USER_ALLOWED_FOR_ALL_PRODUCTS'
        Setting.objects.get(key=key).delete()
    except Exception:
        pass


class Migration(migrations.Migration):
    dependencies = [
     ('settings', '0018_auto_20190429_1604')]
    operations = [
     migrations.RunPython(add_keys, reverse_code=remove_keys)]