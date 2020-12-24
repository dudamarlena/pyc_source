# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_course/migrations/0003_section.py
# Compiled at: 2017-12-21 01:24:44
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_course', '0002_auto_20171218_1738')]
    operations = [
     migrations.CreateModel(name=b'Section', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'name', models.CharField(max_length=180)),
      (
       b'order_by', models.IntegerField(null=True)),
      (
       b'info', models.CharField(max_length=180, null=True))], options={b'ordering': [
                    b'-id'], 
        b'db_table': b'bee_django_course_section'})]