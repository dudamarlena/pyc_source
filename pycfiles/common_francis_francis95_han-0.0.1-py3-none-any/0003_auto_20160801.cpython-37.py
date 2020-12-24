# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/marc/Git/common-framework/common/migrations/0003_auto_20160801.py
# Compiled at: 2018-02-03 12:24:20
# Size of source mod 2**32: 1539 bytes
from __future__ import unicode_literals
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     migrations.swappable_dependency(settings.AUTH_USER_MODEL),
     ('common', '0002_auto_20160531')]
    operations = [
     migrations.CreateModel(name='ServiceUsage',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'name', models.CharField(max_length=100, verbose_name='nom')),
      (
       'count', models.PositiveIntegerField(default=0, verbose_name='nombre')),
      (
       'limit', models.PositiveIntegerField(blank=True, null=True, verbose_name='limite')),
      (
       'address', models.CharField(max_length=40, verbose_name='adresse')),
      (
       'date', models.DateTimeField(auto_now=True, verbose_name='date')),
      (
       'user', models.ForeignKey(on_delete=(django.db.models.deletion.CASCADE), to=(settings.AUTH_USER_MODEL), verbose_name='utilisateur'))],
       options={'verbose_name':'utilisation de service', 
      'verbose_name_plural':'utilisation des services'}),
     migrations.AlterUniqueTogether(name='serviceusage',
       unique_together=(set([('name', 'user')])))]