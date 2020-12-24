# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jordi/vcs/django-multisite/multisite/migrations/0001_initial.py
# Compiled at: 2019-05-02 13:25:00
# Size of source mod 2**32: 1418 bytes
from __future__ import unicode_literals
from __future__ import absolute_import
from django.db import models, migrations
import multisite.models

class Migration(migrations.Migration):
    dependencies = [
     ('sites', '0001_initial')]
    operations = [
     migrations.CreateModel(name='Alias',
       fields=[
      (
       'id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
      (
       'domain', models.CharField(help_text='Either "domain" or "domain:port"', unique=True, max_length=100, verbose_name='domain name')),
      (
       'is_canonical', models.NullBooleanField(default=None, validators=[multisite.models.validate_true_or_none], editable=False, help_text='Does this domain name match the one in site?', verbose_name='is canonical?')),
      (
       'redirect_to_canonical', models.BooleanField(default=True, help_text='Should this domain name redirect to the one in site?', verbose_name='redirect to canonical?')),
      (
       'site', models.ForeignKey(related_name='aliases', to='sites.Site', on_delete=(models.CASCADE)))],
       options={'verbose_name_plural': 'aliases'}),
     migrations.AlterUniqueTogether(name='alias',
       unique_together=(set([('is_canonical', 'site')])))]