# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/arroyo/ovp/suzano-ovp/django-ovp-organizations/ovp_organizations/migrations/0009_organizationinvite.py
# Compiled at: 2017-02-22 17:56:49
# Size of source mod 2**32: 1296 bytes
from __future__ import unicode_literals
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     migrations.swappable_dependency(settings.AUTH_USER_MODEL),
     ('ovp_organizations', '0008_auto_20161207_1941')]
    operations = [
     migrations.CreateModel(name='OrganizationInvite', fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'accepted_date', models.DateTimeField(blank=True, null=True, verbose_name='Deleted date')),
      (
       'created_date', models.DateTimeField(auto_now_add=True)),
      (
       'invitator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='has_invited', to=settings.AUTH_USER_MODEL)),
      (
       'invited', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='been_invited', to=settings.AUTH_USER_MODEL)),
      (
       'organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ovp_organizations.Organization'))])]