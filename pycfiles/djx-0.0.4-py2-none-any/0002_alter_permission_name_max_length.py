# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-n_sfyb/Django/django/contrib/auth/migrations/0002_alter_permission_name_max_length.py
# Compiled at: 2019-02-14 00:35:15
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('auth', '0001_initial')]
    operations = [
     migrations.AlterField(model_name=b'permission', name=b'name', field=models.CharField(max_length=255, verbose_name=b'name'))]