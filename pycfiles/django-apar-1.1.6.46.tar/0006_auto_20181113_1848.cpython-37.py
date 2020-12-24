# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/packages/shops/products/migrations/0006_auto_20181113_1848.py
# Compiled at: 2020-01-05 09:49:45
# Size of source mod 2**32: 399 bytes
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('products', '0005_auto_20181108_1132')]
    operations = [
     migrations.RenameField(model_name='product',
       old_name='is_free',
       new_name='is_free_field')]