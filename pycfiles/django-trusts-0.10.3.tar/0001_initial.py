# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/thomas/Dev/Project/django-trusts/trusts/migrations/0001_initial.py
# Compiled at: 2016-04-16 22:35:57
from __future__ import unicode_literals
from django.db import migrations, models
from django.conf import settings
from django.core.management import call_command
from trusts import ENTITY_MODEL_NAME, GROUP_MODEL_NAME, PERMISSION_MODEL_NAME, DEFAULT_SETTLOR, ALLOW_NULL_SETTLOR, ROOT_PK
import trusts.models

def forward(apps, schema_editor):
    if getattr(settings, b'TRUSTS_CREATE_ROOT', True):
        call_command(b'create_trust_root', apps=apps)


def backward(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
     migrations.swappable_dependency(settings.AUTH_USER_MODEL),
     ('auth', '0006_require_contenttypes_0002')]
    operations = [
     migrations.CreateModel(name=b'Trust', fields=[
      (
       b'id', models.AutoField(verbose_name=b'ID', auto_created=True, primary_key=True, serialize=False)),
      (
       b'title', models.CharField(verbose_name=b'title', max_length=40)),
      (
       b'settlor', models.ForeignKey(to=ENTITY_MODEL_NAME, default=DEFAULT_SETTLOR, null=ALLOW_NULL_SETTLOR)),
      (
       b'trust', models.ForeignKey(to=b'trusts.Trust', related_name=b'trusts_trust_content', default=ROOT_PK)),
      (
       b'groups', models.ManyToManyField(to=GROUP_MODEL_NAME, related_name=b'trusts', verbose_name=b'groups', help_text=b'The groups this trust grants permissions to. A user willget all permissions granted to each of his/her group.'))], options={b'default_permissions': ('add', 'change', 'delete', 'read')}, bases=(
      trusts.models.ReadonlyFieldsMixin, models.Model)),
     migrations.CreateModel(name=b'TrustUserPermission', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, verbose_name=b'ID', serialize=False)),
      (
       b'entity', models.ForeignKey(to=ENTITY_MODEL_NAME, related_name=b'trustpermissions')),
      (
       b'permission', models.ForeignKey(to=PERMISSION_MODEL_NAME, related_name=b'trustentities')),
      (
       b'trust', models.ForeignKey(to=b'trusts.Trust', related_name=b'trustees'))]),
     migrations.CreateModel(name=b'RolePermission', fields=[
      (
       b'id', models.AutoField(verbose_name=b'ID', primary_key=True, serialize=False, auto_created=True)),
      (
       b'managed', models.BooleanField(default=False)),
      (
       b'permission', models.ForeignKey(to=b'auth.Permission', related_name=b'rolepermissions'))]),
     migrations.CreateModel(name=b'Role', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'name', models.CharField(max_length=80, unique=True, help_text=b"The name of the role. Corresponds to the key of model's trusts option.")),
      (
       b'groups', models.ManyToManyField(related_name=b'roles', verbose_name=b'groups', to=b'auth.Group')),
      (
       b'permissions', models.ManyToManyField(to=b'auth.Permission', related_name=b'roles', through=b'trusts.RolePermission', verbose_name=b'permissions'))]),
     migrations.AddField(model_name=b'rolepermission', name=b'role', field=models.ForeignKey(to=b'trusts.Role', related_name=b'rolepermissions')),
     migrations.AlterUniqueTogether(name=b'trust', unique_together=set([('settlor', 'title')])),
     migrations.AlterUniqueTogether(name=b'rolepermission', unique_together=set([('role', 'permission')])),
     migrations.AlterUniqueTogether(name=b'trustuserpermission', unique_together=set([('trust', 'entity', 'permission')])),
     migrations.RunPython(forward, backward)]