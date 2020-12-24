# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/reviews/migrations/0012_auto_20190626_1555.py
# Compiled at: 2020-01-05 09:49:45
# Size of source mod 2**32: 367 bytes
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('reviews', '0011_auto_20190626_1555')]
    operations = [
     migrations.RenameField(model_name='review',
       old_name='user_obj_2',
       new_name='user_obj')]