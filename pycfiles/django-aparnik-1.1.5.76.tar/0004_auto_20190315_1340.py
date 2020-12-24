# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/packages/shops/cosales/migrations/0004_auto_20190315_1340.py
# Compiled at: 2019-03-15 06:12:01
from __future__ import unicode_literals
from django.db import migrations

def remove_all(apps, schema_editor):
    """
    We can't import the Post model directly as it may be a newer
    version than this migration expects. We use the historical version.
    """
    CoSale = apps.get_model(b'cosales', b'CoSale')
    CoSale.objects.all().delete()
    CoSaleHistory = apps.get_model(b'cosales', b'CoSaleHistory')
    CoSaleHistory.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [
     ('cosales', '0003_auto_20190128_1056')]
    operations = [
     migrations.RunPython(remove_all, reverse_code=migrations.RunPython.noop)]