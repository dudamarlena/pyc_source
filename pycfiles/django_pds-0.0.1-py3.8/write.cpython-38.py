# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/django_pds/core/pds/generic/write.py
# Compiled at: 2020-05-11 10:56:23
# Size of source mod 2**32: 2217 bytes
from django_pds.conf import settings
from django_pds.core.controllers import DefaultPermissionSettingsController
from django_pds.core.controllers import GenericInsertCommandController
security_attributes = settings.SECURITY_ATTRIBUTES
read_only_fields = settings.READ_ONLY_FIELDS

def data_insert(document_name, data_json, user_id=None, ignore_security=False, force_insert=False):
    entity_permission = DefaultPermissionSettingsController()
    can_insert = entity_permission.can_insert(document_name, user_id)
    if can_insert:
        insert_ctrl = GenericInsertCommandController()
        err, data_or_error = insert_ctrl.json_load(data_json)
        if err:
            return (
             True, data_or_error)
        data = data_or_error
        if force_insert:
            already_exists = insert_ctrl.already_exists(document_name, data.get('ItemId', None))
            if already_exists:
                if not force_insert:
                    return (True, "document ItemId already exists, you can't create new collection with the same ItemId, if you want to update, use pds update or upsert method")
        if ignore_security:
            return insert_ctrl.insert_one(document_name, data)
        data_fields = set(data.keys())
        rof = set(read_only_fields)
        common_fields = data_fields.intersection(rof)
        if len(common_fields) > 0:
            fields = ','.join(common_fields)
            return (True, f"the following read only attributes {fields} found in the json data")
        sec_attr = set(security_attributes)
        common_fields = data_fields.intersection(sec_attr)
        if len(common_fields) > 0:
            fields = ','.join(common_fields)
            return (True, f"following security attributes {fields} found in the json data")
        error, permissions = entity_permission.get_document_name_permissions(document_name)
        if error:
            return (
             True, error)
        return insert_ctrl.insert_one(document_name, data, user_id, permissions)
    return (True, "access denied, you don't have sufficient permission to insert data")