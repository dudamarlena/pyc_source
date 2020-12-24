# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/settings/migrations/0004_auto_20181130_1658.py
# Compiled at: 2018-12-03 11:15:34
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
        key = b'LOGO_PROJECT_ICON'
        Setting.objects.get(key=key)
    except Exception:
        Setting.objects.create(title=b'لوگو', key=key, value=b'https://cdn.aparnik.com/static/website/img/logo-persian.png', value_type=b's', is_show=True, is_variable_in_home=True)

    try:
        key = b'SERVER_NAME'
        Setting.objects.get(key=key)
    except Exception:
        Setting.objects.create(title=b'آدرس سایت', key=key, value=b'api.aparnik.com', value_type=b's', is_show=False, is_variable_in_home=False)

    try:
        key = b'SERVER_PORT'
        Setting.objects.get(key=key)
    except Exception:
        Setting.objects.create(title=b'پورت سایت', key=key, value=b'80', value_type=b's', is_show=False, is_variable_in_home=False)

    try:
        key = b'PRODUCT_WALLET_ID'
        Setting.objects.get(key=key)
    except Exception:
        Product = apps.get_model(b'products', b'Product')
        ContentType = apps.get_model(b'contenttypes', b'ContentType')
        product = Product.objects.create(price_fabric=1, title=b'شارژ کیف پول')
        new_ct = ContentType.objects.get_for_model(Product)
        Product.objects.filter(polymorphic_ctype__isnull=True).update(polymorphic_ctype=new_ct)
        Setting.objects.create(title=b'شارژ کیف پول', key=key, value=str(product.id), value_type=b'i', is_show=False, is_variable_in_home=False)

    try:
        key = b'COURSE_LEVEL'
        Setting.objects.get(key=key)
    except Exception:
        Setting.objects.create(title=b'سطح دوره', key=key, value=b'2', value_type=b'i', is_show=False, is_variable_in_home=False)

    try:
        key = b'INVITER_GIFT_CREDITS_PER_PURCHASE'
        Setting.objects.get(key=key)
    except Exception:
        Setting.objects.create(title=b'درصد اعتبار هدیه برای دعوت کننده به ازای هر خرید', key=key, value=b'0', value_type=b'i', is_show=False, is_variable_in_home=False)

    try:
        key = b'INVITER_GIFT_CREDITS'
        Setting.objects.get(key=key)
    except Exception:
        Setting.objects.create(title=b'اعتبار هدیه برای دعوت کننده در بدو قبول دعوت تومان', key=key, value=b'0', value_type=b'i', is_show=False, is_variable_in_home=False)

    try:
        key = b'INVITED_GIFT_CREDITS'
        Setting.objects.get(key=key)
    except Exception:
        Setting.objects.create(title=b'اعتبار هدیه برای دعوت شونده در بدو قبول دعوت تومان', key=key, value=b'0', value_type=b'i', is_show=False, is_variable_in_home=False)

    try:
        key = b'PRICE_FORMAT'
        Setting.objects.get(key=key)
    except Exception:
        Setting.objects.create(title=b'اعتبار هدیه برای دعوت کننده در بدو قبول دعوت تومان', key=key, value=b'%ic=t:%se=,:%cu=t:%gr=3:%tr=True:%abbr=True', value_type=b's', is_show=False, is_variable_in_home=False)

    try:
        key = b'PRICE_PRODUCT_FREE_DESCRIPTION'
        Setting.objects.get(key=key)
    except Exception:
        Setting.objects.create(title=b'عنوان کالاهای رایگان', key=key, value=b'رایگان', value_type=b's', is_show=False, is_variable_in_home=False)

    try:
        key = b'PRICE_PRODUCT_SHARING_DESCRIPTION'
        Setting.objects.get(key=key)
    except Exception:
        Setting.objects.create(title=b'عنوان کالاهایی که دعوت شده اند', key=key, value=b'دعوت شده', value_type=b's', is_show=False, is_variable_in_home=False)

    try:
        key = b'PRICE_PRODUCT_BUY_DESCRIPTION'
        Setting.objects.get(key=key)
    except Exception:
        Setting.objects.create(title=b'عنوان کالاهای خریداری شده', key=key, value=b'خریداری شده', value_type=b's', is_show=False, is_variable_in_home=False)

    try:
        key = b'AWS_ACTIVE'
        Setting.objects.get(key=key)
    except Exception:
        Setting.objects.create(title=b'آمازون', key=key, value=b'AWS_ACTIVE', value_type=b'fr', is_show=False, is_variable_in_home=True)

    try:
        key = b'USER_LOGIN_WITH_PASSWORD'
        Setting.objects.get(key=key)
    except Exception:
        Setting.objects.create(title=b'ورود با رمز عبور', key=key, value=b'USER_LOGIN_WITH_PASSWORD', value_type=b'fr', is_show=False, is_variable_in_home=True)


class Migration(migrations.Migration):
    dependencies = [
     ('settings', '0003_auto_20181125_1109')]
    operations = [
     migrations.RunPython(add_keys, reverse_code=migrations.RunPython.noop)]