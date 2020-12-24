# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/arroyo/ovp/gpa-ovp/django-ovp-users/ovp_users/migrations/0026_userprofile_genre.py
# Compiled at: 2017-05-15 11:01:22
# Size of source mod 2**32: 571 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('ovp_users', '0025_remove_userprofile_public')]
    operations = [
     migrations.AddField(model_name='userprofile', name='genre', field=models.CharField(blank=True, choices=[('male', 'Male'), ('female', 'Female')], default=None, max_length=10, null=True, verbose_name='Genre'))]