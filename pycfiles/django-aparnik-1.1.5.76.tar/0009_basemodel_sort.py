# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/basemodels/migrations/0009_basemodel_sort.py
# Compiled at: 2018-12-14 08:14:47
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('basemodels', '0008_auto_20181211_1552')]
    operations = [
     migrations.AddField(model_name=b'basemodel', name=b'sort', field=models.IntegerField(default=0, verbose_name=b'مرتب سازی'))]