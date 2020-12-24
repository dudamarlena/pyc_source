# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/basemodels/migrations/0010_basemodel_visit_count.py
# Compiled at: 2019-01-31 06:07:32
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('basemodels', '0009_basemodel_sort')]
    operations = [
     migrations.AddField(model_name=b'basemodel', name=b'visit_count', field=models.IntegerField(default=0, verbose_name=b'Visit counter'))]