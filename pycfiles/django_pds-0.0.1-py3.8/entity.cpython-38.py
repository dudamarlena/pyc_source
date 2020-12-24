# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/django_pds/models/entity.py
# Compiled at: 2020-05-11 13:44:30
# Size of source mod 2**32: 315 bytes
from mongoengine import StringField
from django_pds.core.base import SimpleBaseDocument

class Entity(SimpleBaseDocument):
    EntityName = StringField(max_length=120, required=True, null=False)
    PrimaryEntityName = StringField(max_length=120, required=True, null=False)
    meta = {'collection': 'Entities'}