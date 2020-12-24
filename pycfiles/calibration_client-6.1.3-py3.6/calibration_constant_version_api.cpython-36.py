# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/calibration_client/apis/calibration_constant_version_api.py
# Compiled at: 2018-03-12 09:48:15
# Size of source mod 2**32: 1300 bytes
"""CalibrationConstantVersionApi class"""
import json
from ..common.base import Base

class CalibrationConstantVersionApi(Base):

    def create_calibration_constant_version_api(self, ccv):
        api_url = self._CalibrationConstantVersionApi__get_api_url()
        return self.api_post(api_url, data=(json.dumps(ccv)))

    def update_calibration_constant_version_api(self, ccv_id, ccv):
        api_url = self._CalibrationConstantVersionApi__get_api_url(ccv_id)
        return self.api_put(api_url, data=(json.dumps(ccv)))

    def get_calibration_constant_version_by_id_api(self, ccv_id):
        api_url = self._CalibrationConstantVersionApi__get_api_url(ccv_id)
        return self.api_get(api_url, params={})

    def get_all_calibration_constant_versions_by_name_api(self, name):
        api_url = self._CalibrationConstantVersionApi__get_api_url()
        return self.api_get(api_url, params={'name': name})

    def __get_api_url(self, api_specifics=''):
        model_name = 'calibration_constant_versions/'
        return self.get_api_url(model_name, api_specifics)