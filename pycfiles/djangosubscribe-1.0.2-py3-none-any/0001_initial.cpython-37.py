# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\djangosubscribe\src\djangosubscribe\migrations\0001_initial.py
# Compiled at: 2020-02-06 02:55:55
# Size of source mod 2**32: 945 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
     migrations.CreateModel(name='SubscriberModel',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'first_name', models.CharField(blank=True, max_length=12, null=True)),
      (
       'last_name', models.CharField(blank=True, max_length=12, null=True)),
      (
       'username', models.CharField(blank=True, max_length=15, null=True)),
      (
       'age', models.PositiveIntegerField(blank=True, null=True)),
      (
       'mobile_number', models.PositiveIntegerField(blank=True, null=True)),
      (
       'email', models.EmailField(max_length=75))])]