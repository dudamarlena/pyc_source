# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/categories/migrations/0003_remove_category_pages.py
# Compiled at: 2020-01-05 09:49:45
# Size of source mod 2**32: 355 bytes
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('categories', '0002_categorysegment')]
    operations = [
     migrations.RemoveField(model_name='category',
       name='pages')]