# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/reviews/migrations/0008_auto_20190613_1830.py
# Compiled at: 2020-01-05 09:49:45
# Size of source mod 2**32: 396 bytes
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('reviews', '0007_auto_20190613_1829')]
    operations = [
     migrations.RenameField(model_name='review',
       old_name='model_obj2',
       new_name='model_obj')]