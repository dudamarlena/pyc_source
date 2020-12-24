# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/djblets/webapi/resources/group.py
# Compiled at: 2019-06-12 01:17:17
"""Built-in resource representing the Group model."""
from __future__ import unicode_literals
from django.contrib.auth.models import Group
from djblets.webapi.resources.base import WebAPIResource
from djblets.webapi.resources.registry import register_resource_for_model

class GroupResource(WebAPIResource):
    """A default resource for representing a Django Group model."""
    model = Group
    fields = ('id', 'name')
    uri_object_key = b'group_name'
    uri_object_key_regex = b'[A-Za-z0-9_\\-]+'
    model_object_key = b'name'
    autogenerate_etags = True
    allowed_methods = ('GET', )


group_resource = GroupResource()
register_resource_for_model(Group, group_resource)