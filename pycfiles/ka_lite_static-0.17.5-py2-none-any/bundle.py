# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/django-tastypie-legacy/tastypie/bundle.py
# Compiled at: 2018-07-11 18:15:32
from __future__ import unicode_literals
from django.http import HttpRequest

class Bundle(object):
    """
    A small container for instances and converted data for the
    ``dehydrate/hydrate`` cycle.

    Necessary because the ``dehydrate/hydrate`` cycle needs to access data at
    different points.
    """

    def __init__(self, obj=None, data=None, request=None, related_obj=None, related_name=None, objects_saved=None, related_objects_to_save=None, via_uri=False):
        self.obj = obj
        self.data = data or {}
        self.request = request or HttpRequest()
        self.related_obj = related_obj
        self.related_name = related_name
        self.errors = {}
        self.objects_saved = objects_saved or set()
        self.related_objects_to_save = related_objects_to_save or {}
        self.via_uri = via_uri

    def __repr__(self):
        return b"<Bundle for obj: '%s' and with data: '%s'>" % (self.obj, self.data)