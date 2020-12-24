# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-n_sfyb/Django/django/contrib/auth/migrations/0005_alter_user_last_login_null.py
# Compiled at: 2019-02-14 00:35:15
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('auth', '0004_alter_user_username_opts')]
    operations = [
     migrations.AlterField(model_name=b'user', name=b'last_login', field=models.DateTimeField(null=True, verbose_name=b'last login', blank=True))]