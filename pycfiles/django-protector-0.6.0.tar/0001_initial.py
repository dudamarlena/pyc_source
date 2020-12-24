# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/s.lihobabin/projects/protector/django-protector/protector/migrations/0001_initial.py
# Compiled at: 2018-05-03 13:51:19
from __future__ import unicode_literals
from django.db import migrations, models
from django.conf import settings
import mptt.fields

class Migration(migrations.Migration):
    dependencies = [
     ('contenttypes', '0002_remove_content_type_name'),
     ('auth', '0006_require_contenttypes_0002'),
     migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [
     migrations.CreateModel(name=b'GenericGlobalPerm', fields=[
      (
       b'id', models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'roles', models.IntegerField(default=1, verbose_name=b'roles')),
      (
       b'content_type', models.ForeignKey(related_name=b'global_perms', default=1, to=b'contenttypes.ContentType', on_delete=models.CASCADE)),
      (
       b'permission', models.ForeignKey(to=b'auth.Permission', on_delete=models.CASCADE))], options={b'verbose_name': b'global group permission', 
        b'verbose_name_plural': b'global group permissions'}),
     migrations.CreateModel(name=b'GenericUserToGroup', fields=[
      (
       b'id', models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'roles', models.IntegerField(null=True, verbose_name=b'roles', blank=True)),
      (
       b'group_id', models.PositiveIntegerField()),
      (
       b'date_joined', models.DateTimeField(auto_now_add=True, verbose_name=b'date joined')),
      (
       b'group_content_type', models.ForeignKey(to=b'contenttypes.ContentType', on_delete=models.CASCADE)),
      (
       b'responsible', models.ForeignKey(related_name=b'created_group_relations', verbose_name=b'responsible', blank=True, to=settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)),
      (
       b'user', models.ForeignKey(related_name=b'generic_group_relations', to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE))], options={b'verbose_name': b'user to group link', 
        b'verbose_name_plural': b'user to group links'}),
     migrations.CreateModel(name=b'OwnerToPermission', fields=[
      (
       b'id', models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'object_id', models.PositiveIntegerField(default=0, verbose_name=b'object id')),
      (
       b'owner_object_id', models.PositiveIntegerField(verbose_name=b'owner id')),
      (
       b'date_issued', models.DateTimeField(auto_now_add=True, verbose_name=b'date issued')),
      (
       b'roles', models.IntegerField(default=1, verbose_name=b'roles')),
      (
       b'content_type', models.ForeignKey(related_name=b'restriction_group_relations', default=1, verbose_name=b'object type', to=b'contenttypes.ContentType', on_delete=models.CASCADE)),
      (
       b'owner_content_type', models.ForeignKey(related_name=b'restricted_object_relations', verbose_name=b'owner type', to=b'contenttypes.ContentType', on_delete=models.CASCADE)),
      (
       b'permission', models.ForeignKey(related_name=b'generic_restriction_relations', verbose_name=b'permission', to=b'auth.Permission', on_delete=models.CASCADE)),
      (
       b'responsible', models.ForeignKey(related_name=b'created_permission_relations', verbose_name=b'responsible', blank=True, to=settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL))], options={b'permissions': (
                       ('add_permission', 'add permission'), ('view_restricted_objects', 'view restricted objects')), 
        b'verbose_name': b'owner to permission link', 
        b'verbose_name_plural': b'owner to permission links'}),
     migrations.CreateModel(name=b'Restriction', fields=[
      (
       b'id', models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'object_id', models.PositiveIntegerField()),
      (
       b'lft', models.PositiveIntegerField(editable=False, db_index=True)),
      (
       b'rght', models.PositiveIntegerField(editable=False, db_index=True)),
      (
       b'tree_id', models.PositiveIntegerField(editable=False, db_index=True)),
      (
       b'level', models.PositiveIntegerField(editable=False, db_index=True)),
      (
       b'content_type', models.ForeignKey(to=b'contenttypes.ContentType', on_delete=models.CASCADE)),
      (
       b'parent', mptt.fields.TreeForeignKey(related_name=b'children', verbose_name=b'parent object', blank=True, to=b'protector.Restriction', null=True, on_delete=models.SET_NULL))], options={b'verbose_name': b'Object restriction', 
        b'verbose_name_plural': b'Objects restrictions'}),
     migrations.AlterUniqueTogether(name=b'restriction', unique_together=set([('object_id', 'content_type')])),
     migrations.AlterUniqueTogether(name=b'ownertopermission', unique_together=set([('content_type', 'object_id', 'owner_content_type', 'owner_object_id', 'permission')])),
     migrations.AlterIndexTogether(name=b'ownertopermission', index_together=set([('owner_content_type', 'owner_object_id'), ('content_type', 'object_id', 'permission')])),
     migrations.AlterUniqueTogether(name=b'genericusertogroup', unique_together=set([('group_id', 'group_content_type', 'user')])),
     migrations.AlterUniqueTogether(name=b'genericglobalperm', unique_together=set([('content_type', 'permission')]))]