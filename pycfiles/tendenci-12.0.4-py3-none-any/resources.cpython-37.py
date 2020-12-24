# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/api_tasty/resources.py
# Compiled at: 2020-02-26 14:47:57
# Size of source mod 2**32: 724 bytes
from tastypie.authorization import Authorization
from tastypie.resources import ModelResource
from tastypie import fields
from tendenci.apps.api_tasty.serializers import SafeSerializer
from tendenci.apps.api_tasty.auth import DeveloperApiKeyAuthentication
from tendenci.apps.api_tasty.users.resources import UserResource

class TendenciResource(ModelResource):
    owner = fields.ForeignKey(UserResource, 'owner')
    creator = fields.ForeignKey(UserResource, 'creator')

    class Meta:
        abstract = True
        object_class = None
        serializer = SafeSerializer()
        authorization = Authorization()
        authentication = DeveloperApiKeyAuthentication()