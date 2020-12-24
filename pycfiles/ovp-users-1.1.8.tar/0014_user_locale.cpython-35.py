# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/arroyo/ovp/gpa-ovp/django-ovp-users/ovp_users/migrations/0014_user_locale.py
# Compiled at: 2017-05-15 11:01:22
# Size of source mod 2**32: 497 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('ovp_users', '0013_auto_20170208_2118')]
    operations = [
     migrations.AddField(model_name='user', name='locale', field=models.CharField(blank=True, default='en', max_length=8, verbose_name='Locale'))]