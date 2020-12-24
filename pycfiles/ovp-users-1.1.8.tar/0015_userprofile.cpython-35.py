# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/arroyo/ovp/gpa-ovp/django-ovp-users/ovp_users/migrations/0015_userprofile.py
# Compiled at: 2017-05-15 11:01:22
# Size of source mod 2**32: 1042 bytes
from __future__ import unicode_literals
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('ovp_core', '0007_lead'),
     ('ovp_users', '0014_user_locale')]
    operations = [
     migrations.CreateModel(name='UserProfile', fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'full_name', models.CharField(blank=True, max_length=300, null=True, verbose_name='Full name')),
      (
       'about', models.TextField(blank=True, null=True, verbose_name='About me')),
      (
       'skills', models.ManyToManyField(to='ovp_core.Skill')),
      (
       'user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL))])]