# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_course/migrations/0029_auto_20180515_1301.py
# Compiled at: 2018-06-14 06:29:04
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_course', '0028_course_image')]
    operations = [
     migrations.AlterField(model_name=b'course', name=b'image', field=models.ImageField(blank=True, null=True, upload_to=b'course/face', verbose_name=b'配图'))]