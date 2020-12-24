# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_course_simple/migrations/0022_part_image.py
# Compiled at: 2019-05-20 08:17:38
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_course_simple', '0021_auto_20190520_2014')]
    operations = [
     migrations.AddField(model_name=b'part', name=b'image', field=models.ImageField(blank=True, null=True, upload_to=b'bee_django_course_simple/part_image', verbose_name=b'配图'))]