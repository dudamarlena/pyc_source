# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/calibration_client/apis/physical_device_api.py
# Compiled at: 2018-03-12 09:48:15
# Size of source mod 2**32: 1164 bytes
"""PhysicalDeviceApi module class"""
import json
from ..common.base import Base

class PhysicalDeviceApi(Base):

    def create_physical_device_api(self, physical_device):
        api_url = self._PhysicalDeviceApi__get_api_url()
        return self.api_post(api_url, data=(json.dumps(physical_device)))

    def delete_physical_device_api(self, physical_device_id):
        api_url = self._PhysicalDeviceApi__get_api_url(physical_device_id)
        return self.api_delete(api_url)

    def update_physical_device_api(self, physical_device_id, physical_device):
        api_url = self._PhysicalDeviceApi__get_api_url(physical_device_id)
        return self.api_put(api_url, data=(json.dumps(physical_device)))

    def get_physical_device_by_id_api(self, physical_device_id):
        api_url = self._PhysicalDeviceApi__get_api_url(physical_device_id)
        return self.api_get(api_url, params={})

    def get_all_physical_devices_by_name_api(self, name):
        api_url = self._PhysicalDeviceApi__get_api_url()
        return self.api_get(api_url, params={'name': name})

    def __get_api_url(self, api_specifics=''):
        model_name = 'physical_devices/'
        return self.get_api_url(model_name, api_specifics)