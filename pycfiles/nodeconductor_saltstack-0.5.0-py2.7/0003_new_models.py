# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nodeconductor_saltstack/sharepoint/migrations/0003_new_models.py
# Compiled at: 2016-09-28 02:05:53
from __future__ import unicode_literals
from django.db import models, migrations
import nodeconductor.core.fields, nodeconductor.core.validators

class Migration(migrations.Migration):
    dependencies = [
     ('sharepoint', '0002_site_tags')]
    operations = [
     migrations.RenameModel(old_name=b'Site', new_name=b'SharepointTenant'),
     migrations.AddField(model_name=b'sharepointtenant', name=b'domain', field=models.CharField(default=b'', max_length=255), preserve_default=False),
     migrations.AddField(model_name=b'sharepointtenant', name=b'admin_login', field=models.CharField(default=b'', blank=True, max_length=255), preserve_default=False),
     migrations.AddField(model_name=b'sharepointtenant', name=b'admin_password', field=models.CharField(default=b'', blank=True, max_length=255), preserve_default=False),
     migrations.AddField(model_name=b'sharepointtenant', name=b'admin_url', field=models.URLField(default=b'', blank=True), preserve_default=False),
     migrations.AddField(model_name=b'sharepointtenant', name=b'site_name', field=models.CharField(default=b'', max_length=255), preserve_default=False),
     migrations.AddField(model_name=b'sharepointtenant', name=b'site_url', field=models.URLField(default=b'', blank=True), preserve_default=False),
     migrations.CreateModel(name=b'Template', fields=[
      (
       b'id', models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'name', models.CharField(max_length=150, verbose_name=b'name', validators=[nodeconductor.core.validators.validate_name])),
      (
       b'uuid', nodeconductor.core.fields.UUIDField()),
      (
       b'backend_id', models.CharField(max_length=255, db_index=True)),
      (
       b'code', models.CharField(max_length=255)),
      (
       b'settings', models.ForeignKey(related_name=b'+', to=b'structure.ServiceSettings'))], options={b'abstract': False}, bases=(
      models.Model,)),
     migrations.CreateModel(name=b'User', fields=[
      (
       b'id', models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'name', models.CharField(max_length=150, verbose_name=b'name', validators=[nodeconductor.core.validators.validate_name])),
      (
       b'uuid', nodeconductor.core.fields.UUIDField()),
      (
       b'backend_id', models.CharField(db_index=True, max_length=255)),
      (
       b'email', models.EmailField(max_length=255)),
      (
       b'username', models.CharField(max_length=255)),
      (
       b'first_name', models.CharField(max_length=255)),
      (
       b'last_name', models.CharField(max_length=255)),
      (
       b'admin_id', models.CharField(max_length=255)),
      (
       b'password', models.CharField(max_length=255)),
      (
       b'tenant', models.ForeignKey(related_name=b'users', to=b'sharepoint.SharepointTenant'))], options={b'abstract': False}, bases=(
      models.Model,)),
     migrations.CreateModel(name=b'Site', fields=[
      (
       b'id', models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'name', models.CharField(max_length=150, verbose_name=b'name')),
      (
       b'uuid', nodeconductor.core.fields.UUIDField()),
      (
       b'backend_id', models.CharField(db_index=True, max_length=255)),
      (
       b'site_url', models.CharField(max_length=255)),
      (
       b'description', models.CharField(max_length=500)),
      (
       b'user', models.ForeignKey(related_name=b'sites', to=b'sharepoint.User'))], options={b'abstract': False}, bases=(
      models.Model,)),
     migrations.AlterUniqueTogether(name=b'template', unique_together=set([('settings', 'backend_id')]))]