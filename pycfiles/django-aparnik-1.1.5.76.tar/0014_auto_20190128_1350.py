# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/settings/migrations/0014_auto_20190128_1350.py
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
        key = b'MANAGER_PRODUCT_ID'
        Setting.objects.get(key=key)
    except Exception:
        Product = apps.get_model(b'products', b'Product')
        ContentType = apps.get_model(b'contenttypes', b'ContentType')
        product = Product.objects.create(price_fabric=1, title=b'محصول مدیریتی', is_show_only_for_super_user=True, aparnik_bon_return_value=1, maximum_use_aparnik_bon_value=1, aparnik_bon_return_expire_value=0)
        new_ct = ContentType.objects.get_for_model(Product)
        Product.objects.filter(polymorphic_ctype__isnull=True).update(polymorphic_ctype=new_ct)
        Setting.objects.create(title=b'آی دی محصول مدیریتی', key=key, value=str(product.id), value_type=b'i', is_show=False, is_variable_in_home=False)


class Migration(migrations.Migration):
    dependencies = [
     ('settings', '0013_auto_20190123_1447')]
    operations = [
     migrations.RunPython(add_keys, reverse_code=migrations.RunPython.noop)]