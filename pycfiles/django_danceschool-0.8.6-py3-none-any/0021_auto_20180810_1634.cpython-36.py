# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /c/Users/Lee/Sync/projects/django-danceschool/currentmaster/django-danceschool/danceschool/core/migrations/0021_auto_20180810_1634.py
# Compiled at: 2019-04-03 22:56:26
# Size of source mod 2**32: 1988 bytes
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('core', '0020_auto_20180808_2247')]
    operations = [
     migrations.CreateModel(name='EventSession',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'name', models.CharField(help_text='Session name will be displayed.', max_length=100, verbose_name='Name')),
      (
       'description', models.TextField(blank=True, help_text='Add an optional description.', null=True, verbose_name='Description')),
      (
       'slug', models.SlugField(help_text='Events can be accessed by a URL based on this slug, as well as by a URL specified by month.', verbose_name='Slug')),
      (
       'startTime', models.DateTimeField(blank=True, help_text='This value should be populated automatically based on the first start time of any event associated with this session.', null=True, verbose_name='Start Time')),
      (
       'endTime', models.DateTimeField(blank=True, help_text='This value should be populated automatically based on the last end time of any event associated with this session.', null=True, verbose_name='End Time'))],
       options={'verbose_name':'Event session', 
      'verbose_name_plural':'Event sessions', 
      'ordering':('startTime', 'name')}),
     migrations.AddField(model_name='event',
       name='session',
       field=models.ForeignKey(blank=True, help_text='Optional event sessions can be used to order events for registration.', null=True, on_delete=(django.db.models.deletion.SET_NULL), to='core.EventSession', verbose_name='Session'))]