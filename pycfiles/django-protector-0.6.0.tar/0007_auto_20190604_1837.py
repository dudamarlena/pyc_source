# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/s.lihobabin/projects/protector/django-protector/protector/migrations/0007_auto_20190604_1837.py
# Compiled at: 2019-07-06 03:37:07
from __future__ import unicode_literals
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('contenttypes', '0002_remove_content_type_name'),
     migrations.swappable_dependency(settings.AUTH_USER_MODEL),
     ('auth', '0008_alter_user_username_max_length'),
     ('protector', '0006_auto_20180726_1229')]
    operations = [
     migrations.CreateModel(name=b'HistoryGenericUserToGroup', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'roles', models.IntegerField(blank=True, null=True, verbose_name=b'roles')),
      (
       b'group_id', models.PositiveIntegerField(verbose_name=b'group id')),
      (
       b'reason', models.TextField(verbose_name=b'change reason')),
      (
       b'changed_at', models.DateTimeField(auto_now_add=True, verbose_name=b'change date')),
      (
       b'change_type', models.SmallIntegerField(choices=[(1, 'add user to group'), (2, 'remove user from group'), (3, 'role changes')])),
      (
       b'group_content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=b'contenttypes.ContentType', verbose_name=b'group content type')),
      (
       b'responsible', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name=b'historygenericusertogroup_created_group_relations', to=settings.AUTH_USER_MODEL, verbose_name=b'responsible')),
      (
       b'user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name=b'historygenericusertogroup_generic_user_relations', to=settings.AUTH_USER_MODEL))], options={b'verbose_name': b'generic user to group history', 
        b'verbose_name_plural': b'generic user to group histories', 
        b'permissions': (('view_generic_group_history', 'view generic group history'), )}),
     migrations.CreateModel(name=b'HistoryOwnerToPermission', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'object_id', models.PositiveIntegerField(null=True, verbose_name=b'object id')),
      (
       b'owner_object_id', models.PositiveIntegerField(verbose_name=b'owner id')),
      (
       b'roles', models.IntegerField(default=1, verbose_name=b'roles')),
      (
       b'reason', models.TextField(verbose_name=b'change reason')),
      (
       b'changed_at', models.DateTimeField(auto_now_add=True, verbose_name=b'change date')),
      (
       b'change_type', models.SmallIntegerField(choices=[(1, 'add permission'), (2, 'remove permission'), (3, 'role changes')])),
      (
       b'content_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name=b'historyownertopermission_restriction_group_relations', to=b'contenttypes.ContentType', verbose_name=b'object type')),
      (
       b'owner_content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name=b'historyownertopermission_restricted_object_relations', to=b'contenttypes.ContentType', verbose_name=b'owner type')),
      (
       b'permission', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name=b'historyownertopermission_generic_restriction_relations', to=b'auth.Permission', verbose_name=b'permission')),
      (
       b'responsible', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name=b'historyownertopermission_responsible', to=settings.AUTH_USER_MODEL, verbose_name=b'responsible'))], options={b'verbose_name': b'owner to permission history', 
        b'verbose_name_plural': b'owner to permission histories', 
        b'permissions': (('view_owner_to_perm_history', 'view owner to permission history'), )}),
     migrations.AlterField(model_name=b'genericusertogroup', name=b'responsible', field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name=b'genericusertogroup_created_group_relations', to=settings.AUTH_USER_MODEL, verbose_name=b'responsible')),
     migrations.AlterField(model_name=b'genericusertogroup', name=b'user', field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name=b'genericusertogroup_generic_user_relations', to=settings.AUTH_USER_MODEL)),
     migrations.AlterField(model_name=b'ownertopermission', name=b'content_type', field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name=b'ownertopermission_restriction_group_relations', to=b'contenttypes.ContentType', verbose_name=b'object type')),
     migrations.AlterField(model_name=b'ownertopermission', name=b'owner_content_type', field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name=b'ownertopermission_restricted_object_relations', to=b'contenttypes.ContentType', verbose_name=b'owner type')),
     migrations.AlterField(model_name=b'ownertopermission', name=b'permission', field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name=b'ownertopermission_generic_restriction_relations', to=b'auth.Permission', verbose_name=b'permission')),
     migrations.AlterField(model_name=b'ownertopermission', name=b'responsible', field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name=b'ownertopermission_responsible', to=settings.AUTH_USER_MODEL, verbose_name=b'responsible'))]