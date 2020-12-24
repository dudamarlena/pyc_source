# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jordi/vcs/django-multisite/multisite/migrations/0001_initial.py
# Compiled at: 2019-05-02 13:25:00
from __future__ import unicode_literals
from __future__ import absolute_import
from django.db import models, migrations
import multisite.models

class Migration(migrations.Migration):
    dependencies = [
     ('sites', '0001_initial')]
    operations = [
     migrations.CreateModel(name=b'Alias', fields=[
      (
       b'id', models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'domain', models.CharField(help_text=b'Either "domain" or "domain:port"', unique=True, max_length=100, verbose_name=b'domain name')),
      (
       b'is_canonical', models.NullBooleanField(default=None, validators=[multisite.models.validate_true_or_none], editable=False, help_text=b'Does this domain name match the one in site?', verbose_name=b'is canonical?')),
      (
       b'redirect_to_canonical', models.BooleanField(default=True, help_text=b'Should this domain name redirect to the one in site?', verbose_name=b'redirect to canonical?')),
      (
       b'site', models.ForeignKey(related_name=b'aliases', to=b'sites.Site', on_delete=models.CASCADE))], options={b'verbose_name_plural': b'aliases'}),
     migrations.AlterUniqueTogether(name=b'alias', unique_together=set([('is_canonical', 'site')]))]