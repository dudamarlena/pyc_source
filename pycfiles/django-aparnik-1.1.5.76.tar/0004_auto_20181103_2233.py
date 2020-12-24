# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/basemodels/migrations/0004_auto_20181103_2233.py
# Compiled at: 2018-11-05 07:19:14
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('basemodels', '0003_basemodel_update_needed')]
    operations = [
     migrations.AlterField(model_name=b'basemodel', name=b'update_needed', field=models.BooleanField(default=False, verbose_name=b'نیاز به بروزرسانی'))]