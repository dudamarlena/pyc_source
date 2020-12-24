# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_course/migrations/0034_auto_20180521_1400.py
# Compiled at: 2018-06-14 06:29:04
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_course', '0033_auto_20180517_1937')]
    operations = [
     migrations.CreateModel(name=b'SectionAttach', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'file', models.FileField(upload_to=b'sections/%Y/%m/%d/', verbose_name=b'附件')),
      (
       b'upload_at', models.DateTimeField(auto_now_add=True)),
      (
       b'section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=b'bee_django_course.Section'))]),
     migrations.AddField(model_name=b'course', name=b'status', field=models.IntegerField(default=0, verbose_name=b'状态'))]