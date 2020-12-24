# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-l2JDtE/django-qcf/qcf/migrations/0001_initial.py
# Compiled at: 2016-10-30 08:08:09
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
     migrations.CreateModel(name=b'Email', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'email', models.EmailField(max_length=254, verbose_name=b'Email')),
      (
       b'subject', models.CharField(max_length=255, verbose_name=b'Subject')),
      (
       b'content', models.TextField(verbose_name=b'Message')),
      (
       b'created', models.DateTimeField(auto_now_add=True, verbose_name=b'Date posted')),
      (
       b'request', models.TextField())], options={b'ordering': ('-created', ), 
        b'verbose_name': b'Email', 
        b'verbose_name_plural': b'Emails'})]