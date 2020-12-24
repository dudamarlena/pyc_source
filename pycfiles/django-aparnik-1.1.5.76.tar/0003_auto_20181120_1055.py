# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/questionanswers/migrations/0003_auto_20181120_1055.py
# Compiled at: 2018-11-21 08:05:12
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('questionanswers', '0002_auto_20181026_1745')]
    operations = [
     migrations.AlterField(model_name=b'qa', name=b'files', field=models.ManyToManyField(blank=True, to=b'filefields.FileField', verbose_name=b'فایل ها'))]