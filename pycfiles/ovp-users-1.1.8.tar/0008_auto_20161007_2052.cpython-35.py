# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/arroyo/ovp/gpa-ovp/django-ovp-users/ovp_users/migrations/0008_auto_20161007_2052.py
# Compiled at: 2016-11-29 13:10:11
# Size of source mod 2**32: 1214 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('auth', '0008_alter_user_username_max_length'),
     ('ovp_users', '0007_auto_20161005_1741')]
    operations = [
     migrations.AddField(model_name='user', name='groups', field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
     migrations.AddField(model_name='user', name='is_superuser', field=models.BooleanField(default=False, verbose_name='Superuser')),
     migrations.AddField(model_name='user', name='user_permissions', field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'))]