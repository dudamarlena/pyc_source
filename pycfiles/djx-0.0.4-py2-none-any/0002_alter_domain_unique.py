# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-n_sfyb/Django/django/contrib/sites/migrations/0002_alter_domain_unique.py
# Compiled at: 2019-02-14 00:35:17
from __future__ import unicode_literals
import django.contrib.sites.models
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('sites', '0001_initial')]
    operations = [
     migrations.AlterField(model_name=b'site', name=b'domain', field=models.CharField(max_length=100, unique=True, validators=[django.contrib.sites.models._simple_domain_name_validator], verbose_name=b'domain name'))]