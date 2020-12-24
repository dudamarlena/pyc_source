# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/irekua_rest_api/tests/test_device_types.py
# Compiled at: 2019-10-28 01:56:48
# Size of source mod 2**32: 906 bytes
from uuid import uuid4
from rest_framework.test import APITestCase
from irekua_rest_api.serializers import device_types
from .utils import BaseTestCase, Users, Actions, create_permission_mapping_from_lists

class DeviceTypeTestCase(BaseTestCase, APITestCase):
    serializer = device_types.CreateSerializer
    permissions = create_permission_mapping_from_lists({Actions.LIST: Users.ALL_AUTHENTICATED_USERS, 
     Actions.CREATE: [
                      Users.ADMIN], 
     
     Actions.RETRIEVE: Users.ALL_AUTHENTICATED_USERS, 
     Actions.UPDATE: [
                      Users.ADMIN], 
     
     Actions.PARTIAL_UPDATE: [
                              Users.ADMIN], 
     
     Actions.DESTROY: [
                       Users.ADMIN]})

    @staticmethod
    def generate_random_json_data():
        data = {'name':str(uuid4()), 
         'description':'Random device type'}
        return data