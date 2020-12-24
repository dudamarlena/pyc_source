# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/calibration_client/apis/physical_device_api.py
# Compiled at: 2018-03-12 09:48:15
# Size of source mod 2**32: 1164 bytes
__doc__ = 'PhysicalDeviceApi module class'
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