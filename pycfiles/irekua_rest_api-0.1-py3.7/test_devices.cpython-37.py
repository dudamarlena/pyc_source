# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/irekua_rest_api/tests/test_devices.py
# Compiled at: 2019-10-28 01:56:48
# Size of source mod 2**32: 1428 bytes
from uuid import uuid4
from rest_framework.test import APITestCase
from irekua_database.utils import simple_JSON_schema
from irekua_database.models import DeviceType, DeviceBrand
from irekua_rest_api.serializers import devices
from .utils import BaseTestCase, Users, Actions, create_permission_mapping_from_lists

class DeviceTestCase(BaseTestCase, APITestCase):
    serializer = devices.CreateSerializer
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
        super().setUp()
        self.device_type = DeviceType.objects.create(name=(str(uuid4())),
          description='random device type')
        self.brand = DeviceBrand.objects.create(name=(str(uuid4())))

    def generate_random_json_data(self):
        data = {'device_type':self.device_type.pk, 
         'brand':self.brand.pk, 
         'model':str(uuid4()), 
         'metadata_schema':simple_JSON_schema(), 
         'configuration_schema':simple_JSON_schema()}
        return data