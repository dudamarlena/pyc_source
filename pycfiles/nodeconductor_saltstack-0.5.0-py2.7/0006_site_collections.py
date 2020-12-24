# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nodeconductor_saltstack/sharepoint/migrations/0006_site_collections.py
# Compiled at: 2016-09-28 02:05:53
from __future__ import unicode_literals
from django.db import models, migrations
import nodeconductor.core.fields, nodeconductor.core.validators

class Migration(migrations.Migration):
    dependencies = [
     ('sharepoint', '0005_sharepointtenant_users_count')]
    operations = [
     migrations.CreateModel(name=b'SiteCollection', fields=[
      (
       b'id', models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'name', models.CharField(max_length=150, verbose_name=b'name', validators=[nodeconductor.core.validators.validate_name])),
      (
       b'uuid', nodeconductor.core.fields.UUIDField()),
      (
       b'backend_id', models.CharField(max_length=255, db_index=True)),
      (
       b'site_url', models.CharField(max_length=255)),
      (
       b'description', models.CharField(max_length=500)),
      (
       b'access_url', models.CharField(max_length=255, blank=True)),
      (
       b'template', models.ForeignKey(related_name=b'site_collections', to=b'sharepoint.Template')),
      (
       b'user', models.ForeignKey(related_name=b'site_collections', to=b'sharepoint.User'))], options={b'abstract': False}, bases=(
      models.Model,)),
     migrations.RemoveField(model_name=b'site', name=b'user'),
     migrations.DeleteModel(name=b'Site'),
     migrations.RemoveField(model_name=b'sharepointtenant', name=b'admin_login'),
     migrations.RemoveField(model_name=b'sharepointtenant', name=b'admin_password'),
     migrations.RemoveField(model_name=b'sharepointtenant', name=b'admin_url'),
     migrations.RemoveField(model_name=b'sharepointtenant', name=b'site_name'),
     migrations.RemoveField(model_name=b'sharepointtenant', name=b'site_url'),
     migrations.RemoveField(model_name=b'sharepointtenant', name=b'storage_size'),
     migrations.RemoveField(model_name=b'sharepointtenant', name=b'user_count'),
     migrations.AddField(model_name=b'sharepointtenant', name=b'admin_site_collection', field=models.ForeignKey(related_name=b'+', blank=True, to=b'sharepoint.SiteCollection', null=True), preserve_default=True),
     migrations.AddField(model_name=b'sharepointtenant', name=b'initialization_status', field=models.CharField(default=b'Not initialized', max_length=20, choices=[('Not initialized', 'Not initialized'), ('Initializing', 'Initializing'), ('Initialized', 'Initialized'), ('Initialization failed', 'Initialization failed')]), preserve_default=True),
     migrations.AddField(model_name=b'sharepointtenant', name=b'main_site_collection', field=models.ForeignKey(related_name=b'+', blank=True, to=b'sharepoint.SiteCollection', null=True), preserve_default=True),
     migrations.AddField(model_name=b'sharepointtenant', name=b'users_site_collection', field=models.ForeignKey(related_name=b'+', blank=True, to=b'sharepoint.SiteCollection', null=True), preserve_default=True)]