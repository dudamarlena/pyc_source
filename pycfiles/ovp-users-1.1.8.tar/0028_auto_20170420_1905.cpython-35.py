# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/arroyo/ovp/gpa-ovp/django-ovp-users/ovp_users/migrations/0028_auto_20170420_1905.py
# Compiled at: 2017-05-15 11:01:22
# Size of source mod 2**32: 586 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('ovp_users', '0027_auto_20170418_1911')]
    operations = [
     migrations.AlterField(model_name='userprofile', name='gender', field=models.CharField(choices=[('male', 'Male'), ('female', 'Female'), ('unspecified', 'Unspecified')], default='unspecified', max_length=20, verbose_name='Gender'))]