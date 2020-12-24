# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/managements/migrations/0002_auto_20181105_2023.py
# Compiled at: 2018-11-26 04:53:01
from __future__ import unicode_literals
from django.db import migrations
from django.apps import apps
from django.db import transaction
from django.utils import timezone

def insert_db_actions(apps, schema_editor):
    ManagementActions = apps.get_model(b'managements', b'ManagementActions')
    ManagementActions.objects.create(title=b'Delete_update', description=b'Delete action')


def insert_db_permisions(apps, schema_editor):
    ManagementPermission = apps.get_model(b'managements', b'ManagementPermission')
    ManagementPermission.objects.create(title=b'view_permission', description=b'change permission')
    ManagementPermission.objects.create(title=b'edit_permission', description=b'edit permission')


def insert_db_fields(apps, schema_editor):
    FieldList = apps.get_model(b'managements', b'FieldList')
    managementActions = apps.get_model(b'managements', b'ManagementActions').objects.all()
    managementPermission = apps.get_model(b'managements', b'ManagementPermission').objects.all()
    for app in apps.get_models():
        for name in app._meta.get_fields(include_parents=True):
            with transaction.atomic():
                field_type = name.get_internal_type()
                if field_type in ('ForeignKey', 'ManyToManyField', 'OneToOneField'):
                    default_value = None
                if field_type in ('FloatField', 'DecimalField', 'PositiveIntegerField',
                                  'IntegerField', 'BooleanField', 'CharField', 'TextField'):
                    default_value = None
                if field_type in b'DateTimeField':
                    default_value = None
                if field_type in b'AutoField':
                    default_value = None
                if name.name in ('publish_day', 'publish_week', 'publish_month'):
                    default_value = None
                field = FieldList.objects.create(model=app._meta.object_name, name=name.name, is_enable=True, is_sharable=False, default=default_value)
                for permission in managementPermission:
                    field.permission.add(permission)

                for action in managementActions:
                    field.actions.add(action)

    return


def insert_db_management(apps, schema_editor):
    Management = apps.get_model(b'managements', b'Management')
    for app in apps.get_app_configs():
        appModels = [ model._meta.object_name for model in list(app.get_models(app.label)) ]
        fieldList = apps.get_model(b'managements', b'FieldList').objects.filter(model__in=appModels)
        if len(appModels) > 0 and len(fieldList) > 0:
            with transaction.atomic():
                Group = apps.get_model(b'auth', b'Group')
                try:
                    group = Group.objects.get(pk=1)
                except:
                    Group.objects.bulk_create([
                     Group(name=b'group11111')])

                management = Management(group_id=1, application=app.label, start_date=timezone.now(), is_active=True)
                management.save({b'is_superuser': True})
                for field in fieldList:
                    management.fields.add(field)


class Migration(migrations.Migration):
    dependencies = [('managements', '0001_initial')]
    operations = [
     migrations.RunPython(insert_db_permisions, reverse_code=migrations.RunPython.noop),
     migrations.RunPython(insert_db_actions, reverse_code=migrations.RunPython.noop),
     migrations.RunPython(insert_db_fields, reverse_code=migrations.RunPython.noop),
     migrations.RunPython(insert_db_management, reverse_code=migrations.RunPython.noop)]