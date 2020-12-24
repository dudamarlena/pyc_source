# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/irekua_rest_api/tests/test_sites.py
# Compiled at: 2019-10-28 01:56:48
# Size of source mod 2**32: 1700 bytes
from uuid import uuid4
from rest_framework.test import APITestCase
from irekua_database.models import SiteType, User
from irekua_database.utils import simple_JSON_schema
from irekua_rest_api.serializers import sites
from .utils import BaseTestCase, Users, Actions, create_permission_mapping_from_lists

class SiteTestCase(BaseTestCase, APITestCase):
    serializer = sites.CreateSerializer
    permissions = create_permission_mapping_from_lists({Actions.LIST: Users.ALL_AUTHENTICATED_USERS, 
     Actions.CREATE: Users.ALL_AUTHENTICATED_USERS, 
     Actions.RETRIEVE: Users.ALL_AUTHENTICATED_USERS, 
     Actions.UPDATE: [
                      Users.ADMIN], 
     
     Actions.PARTIAL_UPDATE: [
                              Users.ADMIN], 
     
     Actions.DESTROY: [
                       Users.ADMIN]})

    def setUp(self):
        super(SiteTestCase, self).setUp()
        self.random_user = User.objects.create(username=(str(uuid4())),
          password=(str(uuid4())))
        self.site_type = SiteType.objects.create(name=(str(uuid4())),
          description='Random Site Type',
          metadata_schema=(simple_JSON_schema()))

    def get_serializer_context(self):

        class DummyRequest(object):

            def __init__(self, user):
                self.user = user

        request = DummyRequest(user=(self.random_user))
        return {'request': request}

    def generate_random_json_data(self):
        data = {'name':str(uuid4()), 
         'site_type':self.site_type.name, 
         'metadata':{},  'longitude':0, 
         'latitude':0}
        return data