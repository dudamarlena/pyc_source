# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_course/migrations/0066_auto_20190816_1757.py
# Compiled at: 2019-08-16 05:57:08
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_course', '0065_auto_20190813_1743')]
    operations = [
     migrations.AddField(model_name=b'usercoursesection', name=b'learned_at', field=models.DateTimeField(blank=True, null=True, verbose_name=b'开始学习时间')),
     migrations.AddField(model_name=b'usercoursesection', name=b'minus_mins', field=models.IntegerField(default=0, verbose_name=b'扣减的时间')),
     migrations.AddField(model_name=b'usercoursesection', name=b'passed_at', field=models.DateTimeField(blank=True, null=True, verbose_name=b'课件通过时间')),
     migrations.AddField(model_name=b'usercoursesection', name=b'send_message_at', field=models.DateTimeField(blank=True, null=True, verbose_name=b'给助教发消息时间')),
     migrations.AddField(model_name=b'usercoursesection', name=b'teacher_add_at', field=models.DateTimeField(blank=True, null=True, verbose_name=b'助教操作时间')),
     migrations.AddField(model_name=b'usercoursesection', name=b'teacher_add_mins', field=models.IntegerField(blank=True, null=True, verbose_name=b'助教增加的练习时间'))]