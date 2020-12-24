# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_course/migrations/0044_sectionvideo_order.py
# Compiled at: 2018-07-07 06:48:31
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_course', '0043_auto_20180625_1928')]
    operations = [
     migrations.AddField(model_name=b'sectionvideo', name=b'order', field=models.IntegerField(default=0, verbose_name=b'在课件里的排序'))]