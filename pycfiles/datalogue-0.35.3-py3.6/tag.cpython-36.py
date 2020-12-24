# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/datalogue/models/tag.py
# Compiled at: 2020-05-13 11:17:34
# Size of source mod 2**32: 1633 bytes
from datetime import datetime
from typing import Optional, Union, List
from uuid import UUID
from datalogue.errors import DtlError
from datalogue.dtl_utils import map_option, _parse_uuid, _parse_datetime

class Tag:
    __doc__ = '\n    A unique tag of metadata that can be applied to datastores for targeted collection, viewing, and action orchestrations\n    '

    def __init__(self, name: str, id: Optional[UUID]=None, created_at: Optional[datetime]=None, created_by: Optional[UUID]=None):
        self.id = id
        self.name = name
        self.created_at = created_at
        self.created_by = created_by

    def __eq__(self, other):
        return self.name == other.name and self.created_at == other.created_at and self.created_by == other.created_by

    def __repr__(self):
        return f"{self.__class__.__name__}(\nid: {self.id!r},\n name: {self.name!r},\ncreated_at: {self.created_at!r},\ncreated_by: UUID({self.created_by!r})\n)"

    @staticmethod
    def _from_payload(payload: dict) -> Union[(DtlError, 'Tag')]:
        name = payload.get('name')
        if name is None:
            return DtlError("'name' is missing for a tag")
        else:
            id = map_option(payload.get('id'), _parse_uuid)
            created_at = payload.get('createdAt')
            created_by = payload.get('createdBy')
            if isinstance(created_at, DtlError):
                return created_at
            return Tag(name, id, created_at, created_by)