# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/basemodels/migrations/0005_basemodel_is_show_only_for_super_user.py
# Compiled at: 2018-12-11 08:51:05
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('basemodels', '0004_auto_20181103_2233')]
    operations = [
     migrations.AddField(model_name=b'basemodel', name=b'is_show_only_for_super_user', field=models.BooleanField(default=False, verbose_name=b'Show only for super user'))]