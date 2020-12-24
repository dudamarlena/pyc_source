# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/joe/workspace/python/klient/src/django-caldav/django_caldav/resources.py
# Compiled at: 2014-08-22 06:39:00
from django.utils.timezone import now
from djangodav.db.resources import NameLookupDBDavMixIn, BaseDBDavResource
from .models import CollectionModel, ObjectModel

class CalDavResource(NameLookupDBDavMixIn, BaseDBDavResource):
    collection_model = CollectionModel
    object_model = ObjectModel