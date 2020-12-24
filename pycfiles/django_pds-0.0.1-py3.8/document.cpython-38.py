# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/django_pds/core/base/document.py
# Compiled at: 2020-05-09 00:25:08
# Size of source mod 2**32: 1588 bytes
from django.utils.timezone import now
from mongoengine import Document, StringField, ListField, DateTimeField

class SimpleBaseDocument(Document):
    ItemId = StringField(required=True, max_length=36, db_field='_id')
    meta = {'allow_inheritance':False, 
     'abstract':True, 
     'strict':True}

    def __str__(self):
        return self.ItemId


class BaseDocument(SimpleBaseDocument):
    CreatedBy = StringField(required=True, max_length=36)
    CreateDate = DateTimeField(default=now)
    Language = StringField(required=True, default='en-US')
    LastUpdateDate = DateTimeField(default=now)
    LastUpdateBy = StringField(required=False)
    Tags = ListField(StringField(min_length=3), default=[])
    IdsAllowedToRead = ListField(StringField(max_length=36), default=[])
    IdsAllowedToWrite = ListField(StringField(max_length=36), default=[])
    IdsAllowedToUpdate = ListField(StringField(max_length=36), default=[])
    IdsAllowedToDelete = ListField(StringField(max_length=36), default=[])
    RolesAllowedToRead = ListField(StringField(max_length=36), default=[])
    RolesAllowedToWrite = ListField(StringField(max_length=36), default=[])
    RolesAllowedToUpdate = ListField(StringField(max_length=36), default=[])
    RolesAllowedToDelete = ListField(StringField(max_length=36), default=[])
    meta = {'allow_inheritance':False, 
     'abstract':True, 
     'strict':True}

    @classmethod
    def pre_save(cls, sender, document, **kwargs):
        document.CreateDate = now()
        document.LastUpdateDate = now()