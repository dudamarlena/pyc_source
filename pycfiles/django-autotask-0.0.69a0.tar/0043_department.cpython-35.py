# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/sam/git/Kanban/django-autotask/djautotask/migrations/0043_department.py
# Compiled at: 2020-02-06 12:23:31
# Size of source mod 2**32: 697 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('djautotask', '0042_auto_20200205_1455')]
    operations = [
     migrations.CreateModel(name='Department', fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'name', models.CharField(max_length=100)),
      (
       'description', models.TextField(blank=True, max_length=1000, null=True)),
      (
       'number', models.CharField(blank=True, max_length=50, null=True))])]