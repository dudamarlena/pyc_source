# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/datalogue/models/permission.py
# Compiled at: 2020-05-13 11:17:34
# Size of source mod 2**32: 6433 bytes
from typing import Union
from datalogue.errors import DtlError, _enum_parse_error
from datalogue.dtl_utils import SerializableStringEnum
from datalogue.models.scope_level import Scope
from uuid import UUID

class Permission(SerializableStringEnum):
    __doc__ = '\n    Class that handles all permission types\n    '
    Share = 'Share'
    Write = 'Write'
    Read = 'Read'

    @staticmethod
    def parse_error(s: str) -> str:
        return DtlError(_enum_parse_error('permission type', s))

    @staticmethod
    def from_string(string: str) -> Union[(DtlError, 'Permission')]:
        return SerializableStringEnum.from_str(Permission)(string)


class OntologyPermission(SerializableStringEnum):
    __doc__ = '\n    Class that handles Ontology permission types\n    '
    Write = 'Write'
    Read = 'Read'

    @staticmethod
    def parse_error(s: str) -> str:
        return DtlError(_enum_parse_error('Ontology permission type', s))

    @staticmethod
    def from_string(string: str) -> Union[(DtlError, 'OntologyPermission')]:
        return SerializableStringEnum.from_str(OntologyPermission)(string)


class CredentialPermission(SerializableStringEnum):
    __doc__ = '\n    Class that handles Credential permission types\n    '
    Write = 'Write'
    Use = 'Use'
    Read = 'Read'

    @staticmethod
    def parse_error(s: str) -> str:
        return DtlError(_enum_parse_error('permission type', s))

    @staticmethod
    def from_string(string: str) -> Union[(DtlError, 'CredentialPermission')]:
        return SerializableStringEnum.from_str(CredentialPermission)(string)


class ObjectType(SerializableStringEnum):
    __doc__ = '\n    Class that handles object types\n    '
    Regex = 'Regex'
    Classifier = 'Classifier'
    Tag = 'Tag'
    PipelineTemplate = 'PipelineTemplate'

    @staticmethod
    def parse_error(s: str) -> str:
        return DtlError(_enum_parse_error('object type', s))

    @staticmethod
    def from_string(string: str) -> Union[(DtlError, 'ObjectType')]:
        return SerializableStringEnum.from_str(ObjectType)(string)


class SharePermission:
    __doc__ = '\n    This is a class that represents an object permission.\n\n    Attributes:\n        target_id (UUID): the uuid of the User, Group or Organization..\n        target_type (Scope): the target you are sharing with. It can be a User, Group or Organization.\n        permission (Permission): the type of permission you want to grant. It can be Read, Write or Share.\n    '

    def __init__(self, object_type: ObjectType, target_id: UUID=None, target_type: Scope=None, permission: Permission=None):
        """
        The constructor for Share class.

        Parameters:
            object_type (ObjectType): the type of object
            target_id (UUID): the uuid of the User, Group or Organization..
            target_type (Scope): the target you are sharing with. It can be a User, Group or Organization.
            permission (Permission): the type of permission you want to grant. It can be Read, Write or Share.
        """
        self.object_type = object_type
        self.target_id = target_id
        self.target_type = target_type
        self.permission = permission

    def __repr__(self):
        return f"{self.permission!r} permissions for this {self.object_type!r} are extended to target {self.target_type!r} with id: {self.target_id!r}"

    def from_payload(self, payload: dict) -> Union[(DtlError, 'SharePermission')]:
        target_id = payload.get('targetId')
        if target_id is None or not isinstance(target_id, str):
            return DtlError("'targetId' is missing or not a string")
        target_type = payload.get('targetType')
        if target_type is None or not isinstance(target_type, str):
            return DtlError("'targetType' is missing or not a string")
        else:
            permission = payload.get('permission')
            if permission is None or not isinstance(permission, str):
                return DtlError("'permission' is missing or not a string")
            return SharePermission(self.object_type, target_id, target_type, permission)


class UnsharePermission:
    __doc__ = '\n    This is a class that represents an object permission removal.\n    Attributes:\n        target_id (UUID): the uuid of the User, Group or Organization..\n        target_type (Scope): the target you are unsharing with. It can be a User, Group or Organization.\n        permission (Permission): the type of permission you want to remove. It can be Read, Write or Share.\n    '

    def __init__(self, object_type: ObjectType, target_id: UUID=None, target_type: Scope=None, permission: Permission=None):
        """
        The constructor for Unshare class.
        Parameters:
            object_type (ObjectType): the type of object
            target_id (UUID): the uuid of the User, Group or Organization..
            target_type (Scope): the target you are unsharing with. It can be a User, Group or Organization.
            permission (Permission): the type of permission you want to remove. It can be Read, Write or Share.
        """
        self.object_type = object_type
        self.target_id = target_id
        self.target_type = target_type
        self.permission = permission

    def __repr__(self):
        return f"{self.permission!r} permissions for this {self.object_type!r} are withdrawn from target {self.target_type!r} with id: {self.target_id!r}"

    def from_payload(self, payload: dict) -> Union[(DtlError, 'UnsharePermission')]:
        target_id = payload.get('targetId')
        if target_id is None or not isinstance(target_id, str):
            return DtlError("'targetId' is missing or not a string")
        target_type = payload.get('targetType')
        if target_type is None or not isinstance(target_type, str):
            return DtlError("'targetType' is missing or not a string")
        else:
            permission = payload.get('permission')
            if permission is None or not isinstance(permission, str):
                return DtlError("'permission' is missing or not a string")
            return UnsharePermission(self.object_type, target_id, target_type, permission)