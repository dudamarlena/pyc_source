# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/settings/migrations/0003_auto_20181125_1109.py
# Compiled at: 2018-11-25 03:12:47
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('settings', '0002_auto_20181125_1057')]
    operations = [
     migrations.AlterField(model_name=b'setting', name=b'value', field=models.TextField(verbose_name=b'Value'))]