# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/settings/migrations/0005_auto_20181130_1938.py
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
        key = b'APARNIK_BON_VALUE'
        Setting.objects.get(key=key)
    except Exception:
        Setting.objects.create(title=b'ارزش تومانی هر بن', key=key, value=b'100', value_type=b'i', is_show=True, is_variable_in_home=True)

    try:
        key = b'APARNIK_BON_RETURN_DEFAULT_VALUE'
        Setting.objects.get(key=key)
    except Exception:
        Setting.objects.create(title=b'مقدار بن پیش فرضی برای هر محصول پس از خرید که به کاربر باز گردانده می شود. ', key=key, value=b'0', value_type=b'i', is_show=True, is_variable_in_home=False)

    try:
        key = b'APARNIK_BON_RETURN_DEFAULT_EXPIRE_VALUE'
        Setting.objects.get(key=key)
    except Exception:
        Setting.objects.create(title=b'کاربر تا چه زمانی می تواند از بن بدست آمده از خرید یک محصول استفاده کند. عدد ۰ به معنای عدم محدودیت است. واحد ساعت است.', key=key, value=b'0', value_type=b'i', is_show=True, is_variable_in_home=False)

    try:
        key = b'MAXIMUM_USE_APARNIK_BON'
        Setting.objects.get(key=key)
    except Exception:
        Setting.objects.create(title=b'مقدار پیش فرض استفاده بن برای خرید هر کالا', key=key, value=b'-2', value_type=b'i', is_show=True, is_variable_in_home=False)

    try:
        key = b'HAS_PERMIT_DEFAULT_USE_WALLET'
        Setting.objects.get(key=key)
    except Exception:
        Setting.objects.create(title=b'مقدار پیش فرض اجازه پرداخت با کیف پول در هر کالا', key=key, value=b'True', value_type=b'b', is_show=True, is_variable_in_home=False)

    key = b'INVITER_GIFT_CREDITS'
    inviter_gift_credits = Setting.objects.get(key=key)
    inviter_gift_credits.key = b'INVITER_GIFT_BON_CREDITS'
    inviter_gift_credits.title = b'بن هدیه برای دعوت کننده در بدو قبول دعوت'
    inviter_gift_credits.save()
    key = b'INVITED_GIFT_CREDITS'
    invited_gift_credits = Setting.objects.get(key=key)
    invited_gift_credits.key = b'INVITED_GIFT_BON_CREDITS'
    invited_gift_credits.title = b'بن هدیه برای دعوت شونده در بدو قبول دعوت'
    invited_gift_credits.save()


class Migration(migrations.Migration):
    dependencies = [
     ('settings', '0004_auto_20181130_1658')]
    operations = [
     migrations.RunPython(add_keys, reverse_code=migrations.RunPython.noop)]