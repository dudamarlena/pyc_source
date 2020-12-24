# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/django_pds/models/role.py
# Compiled at: 2020-05-11 13:10:12
# Size of source mod 2**32: 313 bytes
from mongoengine import StringField, ListField, BooleanField
from django_pds.core.base import SimpleBaseDocument

class Role(SimpleBaseDocument):
    RoleName = StringField(required=True)
    ParentRoles = ListField(StringField())
    IsDynamic = BooleanField(default=False)
    meta = {'collection': 'Roles'}