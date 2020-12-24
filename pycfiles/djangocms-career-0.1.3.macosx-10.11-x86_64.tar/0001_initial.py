# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dominicmonn/Documents/Private/cms-sample/dev_packages/djangocms-career/djangocms_career/migrations/0001_initial.py
# Compiled at: 2016-04-18 05:23:47
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = []
    operations = [
     migrations.CreateModel(name=b'Position', fields=[
      (
       b'id', models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'start_date', models.DateField(help_text=b'The date when you started this position - only the month and year will be displayed', verbose_name=b'Start date')),
      (
       b'end_date', models.DateField(help_text=b"The date when this position ended - only the month and year will be displayed. You don't have to define this if it is your active post.", null=True, verbose_name=b'End date', blank=True)),
      (
       b'is_active', models.BooleanField(help_text=b"Check this if this is your active post. You won't have to add the end_date in that case.", verbose_name=b'Active position?'))], options={b'abstract': False}),
     migrations.CreateModel(name=b'PositionTranslation', fields=[
      (
       b'id', models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'title', models.CharField(max_length=255, verbose_name=b'Title')),
      (
       b'company', models.CharField(max_length=255, verbose_name=b'Company')),
      (
       b'description', models.TextField(help_text=b'Give a short description about your work and responsibilities.', max_length=2048, null=True, verbose_name=b'Description', blank=True)),
      (
       b'website', models.CharField(help_text=b"Provide a link to the company's website.", max_length=255, verbose_name=b'Website')),
      (
       b'language_code', models.CharField(max_length=15, db_index=True)),
      (
       b'master', models.ForeignKey(related_name=b'translations', editable=False, to=b'djangocms_career.Position', null=True))], options={b'managed': True, 
        b'abstract': False, 
        b'db_table': b'djangocms_career_position_translation', 
        b'db_tablespace': b'', 
        b'default_permissions': ()}),
     migrations.AlterUniqueTogether(name=b'positiontranslation', unique_together=set([('language_code', 'master')]))]