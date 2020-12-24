# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_course/migrations/0018_auto_20180324_1703.py
# Compiled at: 2018-03-28 03:58:28
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_course', '0017_auto_20180324_0915')]
    operations = [
     migrations.AlterField(model_name=b'userimage', name=b'image', field=models.ImageField(upload_to=b'course/%Y/%m/%d', verbose_name=b'图片'))]