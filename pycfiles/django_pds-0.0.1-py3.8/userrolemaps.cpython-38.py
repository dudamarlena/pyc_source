# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/django_pds/models/userrolemaps.py
# Compiled at: 2020-05-11 13:11:00
# Size of source mod 2**32: 260 bytes
from mongoengine import StringField
from django_pds.core.base import BaseDocument

class UserRoleMap(BaseDocument):
    RoleName = StringField(required=True)
    RoleId = StringField(required=False, max_length=36)
    meta = {'collection': 'UserRoleMaps'}