# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/quincy/Code/valuehorizon-people/people/migrations/0001_initial.py
# Compiled at: 2015-05-08 17:59:14
from __future__ import unicode_literals
from django.db import models, migrations

class Migration(migrations.Migration):
    dependencies = [
     ('countries', '__first__')]
    operations = [
     migrations.CreateModel(name=b'Person', fields=[
      (
       b'id', models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'gender', models.CharField(max_length=1, choices=[('M', 'Male'), ('F', 'Female')])),
      (
       b'title', models.CharField(max_length=10, choices=[('DR', 'Dr.'), ('MR', 'Mr.'), ('MS', 'Ms.'), ('MRS', 'Mrs.'), ('SIR', 'Sir'), ('LORD', 'Lord')])),
      (
       b'first_name', models.CharField(max_length=255)),
      (
       b'last_name', models.CharField(max_length=255)),
      (
       b'other_names', models.CharField(help_text=b'Middle names, comma separated', max_length=255, blank=True)),
      (
       b'date_of_birth', models.DateField(null=True, blank=True)),
      (
       b'date_of_death', models.DateField(null=True, blank=True)),
      (
       b'profile', models.TextField(help_text=b'Description of Person', blank=True)),
      (
       b'is_deceased', models.BooleanField(default=False)),
      (
       b'full_name', models.CharField(max_length=255, editable=False, blank=True)),
      (
       b'date_modified', models.DateTimeField(auto_now=True, null=True)),
      (
       b'date_created', models.DateTimeField(auto_now_add=True, null=True)),
      (
       b'nationality', models.ManyToManyField(related_name=b'nationalities', null=True, to=b'countries.Country', blank=True))], options={b'ordering': [
                    b'last_name', b'first_name', b'date_of_birth'], 
        b'verbose_name': b'Person', 
        b'verbose_name_plural': b'People'})]