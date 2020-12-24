# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ggg/www/dev/mogos/mogo89/mogo/qcf/migrations/0001_initial.py
# Compiled at: 2017-06-14 09:54:15
# Size of source mod 2**32: 1049 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
     migrations.CreateModel(name='Email', fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'email', models.EmailField(max_length=254, verbose_name='Email')),
      (
       'subject', models.CharField(max_length=255, verbose_name='Subject')),
      (
       'content', models.TextField(verbose_name='Message')),
      (
       'created', models.DateTimeField(auto_now_add=True, verbose_name='Date posted')),
      (
       'request', models.TextField())], options={'ordering': ('-created', ), 
      'verbose_name': 'Email', 
      'verbose_name_plural': 'Emails'})]