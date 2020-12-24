# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/asyncee/git/django-cmstemplates/cmstemplates/migrations/0001_initial.py
# Compiled at: 2015-03-22 09:13:48
from __future__ import unicode_literals
from django.db import models, migrations

class Migration(migrations.Migration):
    dependencies = []
    operations = [
     migrations.CreateModel(name=b'Template', fields=[
      (
       b'id', models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'name', models.CharField(help_text=b'Template name, for example, "headline"', max_length=255, verbose_name=b'Template name')),
      (
       b'weight', models.IntegerField(default=0, verbose_name=b'Output order')),
      (
       b'content', models.TextField(verbose_name=b'Content')),
      (
       b'is_active', models.BooleanField(default=True, verbose_name=b'Active')),
      (
       b'only_for_superuser', models.BooleanField(default=False, verbose_name=b'Only for superuser'))], options={b'ordering': [
                    b'weight'], 
        b'verbose_name': b'Template', 
        b'verbose_name_plural': b'Template'}, bases=(
      models.Model,)),
     migrations.CreateModel(name=b'TemplateGroup', fields=[
      (
       b'id', models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'name', models.CharField(max_length=255, verbose_name=b'Template group name')),
      (
       b'description', models.TextField(verbose_name=b'Short description', blank=True))], options={b'verbose_name': b'Template group', 
        b'verbose_name_plural': b'Template groups'}, bases=(
      models.Model,)),
     migrations.AddField(model_name=b'template', name=b'group', field=models.ForeignKey(related_name=b'templates', verbose_name=b'Group', to=b'cmstemplates.TemplateGroup'), preserve_default=True)]