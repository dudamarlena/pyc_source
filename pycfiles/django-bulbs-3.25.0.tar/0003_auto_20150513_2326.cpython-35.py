# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /webapp/bulbs/content/migrations/0003_auto_20150513_2326.py
# Compiled at: 2016-09-22 15:00:17
# Size of source mod 2**32: 1009 bytes
from __future__ import unicode_literals
import django
from django.db import models, migrations

class Migration(migrations.Migration):
    dependencies = [
     ('content', '0002_add_groups')]
    if django.VERSION >= (1, 8, 0):
        dependencies.insert(0, ('contenttypes', '0002_remove_content_type_name'))
    operations = [
     migrations.CreateModel(name='TemplateType', fields=[
      (
       'id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
      (
       'name', models.CharField(max_length=255)),
      (
       'slug', models.SlugField(unique=True)),
      (
       'content_type', models.ForeignKey(to='contenttypes.ContentType'))]),
     migrations.AddField(model_name='content', name='template_type', field=models.ForeignKey(blank=True, to='content.TemplateType', null=True))]