# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/basemodels/migrations/0005_basemodel_is_show_only_for_super_user.py
# Compiled at: 2020-01-05 09:49:45
# Size of source mod 2**32: 481 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('basemodels', '0004_auto_20181103_2233')]
    operations = [
     migrations.AddField(model_name='basemodel',
       name='is_show_only_for_super_user',
       field=models.BooleanField(default=False, verbose_name='Show only for super user'))]