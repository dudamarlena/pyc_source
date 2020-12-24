# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/craiglabenz/Sites/tablets/tablets/migrations/0001_initial.py
# Compiled at: 2016-10-07 11:23:47
# Size of source mod 2**32: 1348 bytes
from __future__ import unicode_literals
from django.db import models, migrations
import jsonfield.fields

class Migration(migrations.Migration):
    dependencies = []
    operations = [
     migrations.CreateModel(name='Template', fields=[
      (
       'id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
      (
       'name', models.CharField(max_length=255)),
      (
       'content', models.TextField(blank=True)),
      (
       'template_engine', models.IntegerField(default=1, verbose_name='Template Engine', choices=[(1, 'Django'), (2, 'Jinja2')])),
      (
       'default_context', jsonfield.fields.JSONField(blank=True, default=dict, help_text='Does not work so well for Jinja2 templates, which throw exceptions for missing values. This can make things tough if your template relies on functions.', verbose_name='Default Context')),
      (
       'parent', models.ForeignKey(related_name='children', blank=True, to='tablets.Template', help_text='Select another template this template should extend.', null=True))], options={'verbose_name': 'Template', 
      'verbose_name_plural': 'Templates'}, bases=(
      models.Model,))]