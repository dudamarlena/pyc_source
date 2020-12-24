# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_course/migrations/0038_auto_20180617_1423.py
# Compiled at: 2018-06-26 00:36:23
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_course', '0037_auto_20180615_1256')]
    operations = [
     migrations.AlterField(model_name=b'usersectionnote', name=b'note', field=models.TextField(verbose_name=b'学习笔记'))]