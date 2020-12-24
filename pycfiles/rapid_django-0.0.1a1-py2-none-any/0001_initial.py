# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/marcos/rapid-django/src/rapid/migrations/0001_initial.py
# Compiled at: 2015-09-18 15:20:20
from __future__ import unicode_literals
from django.db import models, migrations
from django.conf import settings

class Migration(migrations.Migration):
    dependencies = [
     migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [
     migrations.CreateModel(name=b'Application', fields=[
      (
       b'id', models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'name', models.CharField(unique=True, max_length=60, verbose_name=b'nome')),
      (
       b'python_name', models.CharField(unique=True, max_length=255, verbose_name=b'Nome no Python')),
      (
       b'enabled', models.BooleanField(default=True, verbose_name=b'ativa')),
      (
       b'managers', models.ManyToManyField(related_name=b'managed_applications', verbose_name=b'gestores', to=settings.AUTH_USER_MODEL))], options={b'verbose_name': b'aplicação', 
        b'verbose_name_plural': b'aplicações'}),
     migrations.CreateModel(name=b'Profile', fields=[
      (
       b'id', models.AutoField(serialize=False, primary_key=True)),
      (
       b'name', models.CharField(max_length=60, verbose_name=b'nome')),
      (
       b'description', models.TextField(verbose_name=b'descrição')),
      (
       b'application', models.ForeignKey(verbose_name=b'aplicação', to=b'rapid.Application')),
      (
       b'users', models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name=b'usuários', blank=True))], options={b'verbose_name': b'perfil', 
        b'verbose_name_plural': b'perfis'})]