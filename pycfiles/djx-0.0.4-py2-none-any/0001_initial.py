# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-n_sfyb/Django/django/contrib/sites/migrations/0001_initial.py
# Compiled at: 2019-02-14 00:35:17
from __future__ import unicode_literals
import django.contrib.sites.models
from django.contrib.sites.models import _simple_domain_name_validator
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = []
    operations = [
     migrations.CreateModel(name=b'Site', fields=[
      (
       b'id', models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'domain',
       models.CharField(max_length=100, verbose_name=b'domain name', validators=[_simple_domain_name_validator])),
      (
       b'name', models.CharField(max_length=50, verbose_name=b'display name'))], options={b'ordering': ('domain', ), 
        b'db_table': b'django_site', 
        b'verbose_name': b'site', 
        b'verbose_name_plural': b'sites'}, bases=(
      models.Model,), managers=[
      (
       b'objects', django.contrib.sites.models.SiteManager())])]