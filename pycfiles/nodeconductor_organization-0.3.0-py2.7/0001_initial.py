# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nodeconductor_organization/migrations/0001_initial.py
# Compiled at: 2016-09-25 10:50:25
from __future__ import unicode_literals
from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings
import nodeconductor.core.fields, nodeconductor.core.validators

class Migration(migrations.Migration):
    dependencies = [
     ('structure', '0026_add_error_message'),
     migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [
     migrations.CreateModel(name=b'Organization', fields=[
      (
       b'id', models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'name', models.CharField(max_length=150, verbose_name=b'name', validators=[nodeconductor.core.validators.validate_name])),
      (
       b'uuid', nodeconductor.core.fields.UUIDField()),
      (
       b'abbreviation', models.CharField(unique=True, max_length=8)),
      (
       b'native_name', models.CharField(max_length=160, null=True, blank=True)),
      (
       b'customer', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to=b'structure.Customer'))], options={b'abstract': False}, bases=(
      models.Model,)),
     migrations.CreateModel(name=b'OrganizationUser', fields=[
      (
       b'id', models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'uuid', nodeconductor.core.fields.UUIDField()),
      (
       b'is_approved', models.BooleanField(default=False)),
      (
       b'organization', models.ForeignKey(to=b'nodeconductor_organization.Organization')),
      (
       b'user', models.OneToOneField(to=settings.AUTH_USER_MODEL))], options={b'abstract': False}, bases=(
      models.Model,))]