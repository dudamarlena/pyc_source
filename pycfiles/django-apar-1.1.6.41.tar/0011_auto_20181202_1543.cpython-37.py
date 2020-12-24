# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/packages/shops/products/migrations/0011_auto_20181202_1543.py
# Compiled at: 2020-01-05 09:49:45
# Size of source mod 2**32: 1472 bytes
from django.db import migrations

def negative_default_value(apps, schema_editor):
    """
    We can't import the Post model directly as it may be a newer
    version than this migration expects. We use the historical version.
    """
    Object = apps.get_model('products', 'Product')
    Object.objects.filter(aparnik_bon_return_value=0).update(aparnik_bon_return_value=(-1))
    Object.objects.filter(aparnik_bon_return_expire_value=0).update(aparnik_bon_return_expire_value=(-1))
    Object.objects.filter(maximum_use_aparnik_bon_value=0).update(maximum_use_aparnik_bon_value=(-2))
    Object.objects.filter(has_permit_use_wallet_value=0).update(has_permit_use_wallet_value=(-1))


def zero_default_value(apps, schema_editor):
    Object = apps.get_model('products', 'Product')
    Object.objects.filter(aparnik_bon_return_value=(-1)).update(aparnik_bon_return_value=0)
    Object.objects.filter(aparnik_bon_return_expire_value=(-1)).update(aparnik_bon_return_expire_value=0)
    Object.objects.filter(maximum_use_aparnik_bon_value=(-2)).update(maximum_use_aparnik_bon_value=0)
    Object.objects.filter(has_permit_use_wallet_value=(-1)).update(has_permit_use_wallet_value=0)


class Migration(migrations.Migration):
    dependencies = [
     ('products', '0010_auto_20181202_1542')]
    operations = [
     migrations.RunPython(negative_default_value, reverse_code=zero_default_value)]