# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\djangocontact\src\djangocontact\migrations\0001_initial.py
# Compiled at: 2019-10-14 09:08:45
# Size of source mod 2**32: 953 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
     migrations.CreateModel(name='EmailModel',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'email', models.EmailField(max_length=55)),
      (
       'full_name', models.CharField(max_length=20)),
      (
       'content', models.TextField(max_length=250)),
      (
       'created_at', models.DateTimeField(auto_now_add=True)),
      (
       'updated_at', models.DateTimeField(auto_now=True))],
       options={'verbose_name':'Email', 
      'verbose_name_plural':'Emails', 
      'ordering':[
       'pk']})]