# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/arroyo/ovp/suzano-ovp/django-ovp-organizations/ovp_organizations/migrations/0002_organization.py
# Compiled at: 2017-02-22 17:56:49
# Size of source mod 2**32: 2223 bytes
from __future__ import unicode_literals
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = [
     migrations.swappable_dependency(settings.AUTH_USER_MODEL),
     ('ovp_core', '0004_load_skills_and_causes'),
     ('ovp_organizations', '0001_initial')]
    operations = [
     migrations.CreateModel(name='Organization', fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'name', models.CharField(max_length=150, verbose_name='Name')),
      (
       'website', models.URLField(blank=True, default=None, null=True)),
      (
       'facebook_page', models.URLField(blank=True, default=None, null=True)),
      (
       'highlighted', models.BooleanField(default=False, verbose_name='Highlighted')),
      (
       'published', models.BooleanField(default=False, verbose_name='Published')),
      (
       'published_at', models.DateTimeField(blank=True, null=True, verbose_name='Published date')),
      (
       'deleted', models.BooleanField(default=False, verbose_name='Deleted')),
      (
       'deleted_at', models.DateTimeField(blank=True, null=True, verbose_name='Deleted date')),
      (
       'created_at', models.DateTimeField(auto_now_add=True)),
      (
       'modified_at', models.DateTimeField(auto_now=True)),
      (
       'details', models.CharField(blank=True, default=None, max_length=3000, null=True, verbose_name='Details')),
      (
       'description', models.CharField(blank=True, max_length=160, null=True, verbose_name='Short description')),
      (
       'address', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ovp_core.GoogleAddress')),
      (
       'owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL))], options={'verbose_name': 'organization'})]