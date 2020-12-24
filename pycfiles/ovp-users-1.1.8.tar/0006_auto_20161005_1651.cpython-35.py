# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/arroyo/ovp/gpa-ovp/django-ovp-users/ovp_users/migrations/0006_auto_20161005_1651.py
# Compiled at: 2016-11-29 13:10:11
# Size of source mod 2**32: 780 bytes
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('ovp_users', '0005_passwordrecoverytoken_created_date')]
    operations = [
     migrations.AddField(model_name='passwordrecoverytoken', name='used', field=models.DateTimeField(blank=True, default=None, null=True)),
     migrations.AlterField(model_name='passwordrecoverytoken', name='user', field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ovp_users.User'))]