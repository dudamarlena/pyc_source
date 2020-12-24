# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/calibration_client/apis/calibration_constant_api.py
# Compiled at: 2019-08-05 13:13:33
# Size of source mod 2**32: 4139 bytes
"""CalibrationConstantApi class"""
import json
from ..common.base import Base

class CalibrationConstantApi(Base):

    def create_calibration_constant_api(self, cal_constant):
        api_url = self._CalibrationConstantApi__get_api_url()
        return self.api_post(api_url, data=(json.dumps(cal_constant)))

    def delete_calibration_constant_api(self, cal_constant_id):
        api_url = self._CalibrationConstantApi__get_api_url(cal_constant_id)
        return self.api_delete(api_url)

    def update_calibration_constant_api(self, cal_constant_id, cal_constant):
        api_url = self._CalibrationConstantApi__get_api_url(cal_constant_id)
        return self.api_put(api_url, data=(json.dumps(cal_constant)))

    def get_calibration_constant_by_id_api(self, cal_constant_id):
        api_url = self._CalibrationConstantApi__get_api_url(cal_constant_id)
        return self.api_get(api_url, params={})

    def get_all_calibration_constants_by_name_api(self, name):
        api_url = self._CalibrationConstantApi__get_api_url()
        return self.api_get(api_url, params={'name': name})

    def get_calibration_constant_version_by_uk_api(self, calibration_constant_id, physical_device_id, event_at, snapshot_at):
        api_action_name = '/get_version'
        api_relative_url = '{0}{1}'.format(calibration_constant_id, api_action_name)
        api_url = self._CalibrationConstantApi__get_api_url(api_relative_url)
        params = {'physical_device_id':str(physical_device_id), 
         'event_at':event_at, 
         'snapshot_at':snapshot_at}
        self.check_session_token()
        return self.oauth_client.session.get(api_url, headers=(self.headers),
          params=params)

    def get_closest_calibration_constant_version_api(self, calibration_constant_ids, physical_device_id, event_at, snapshot_at):
        api_action_name = '/get_closest_version'
        api_relative_url = '{0}{1}'.format(calibration_constant_ids[0], api_action_name)
        api_url = self._CalibrationConstantApi__get_api_url(api_relative_url)
        params = {'calibration_constant_ids':str(calibration_constant_ids), 
         'physical_device_id':str(physical_device_id), 
         'event_at':event_at, 
         'snapshot_at':snapshot_at}
        self.check_session_token()
        return self.oauth_client.session.get(api_url, headers=(self.headers),
          params=params)

    def get_all_calibration_constant_versions_api(self, calibration_constant_ids, physical_device_id, event_at, snapshot_at):
        api_action_name = '/get_all_versions'
        api_relative_url = '{0}{1}'.format(calibration_constant_ids[0], api_action_name)
        api_url = self._CalibrationConstantApi__get_api_url(api_relative_url)
        params = {'calibration_constant_ids':str(calibration_constant_ids), 
         'physical_device_id':str(physical_device_id), 
         'event_at':event_at, 
         'snapshot_at':snapshot_at}
        self.check_session_token()
        return self.oauth_client.session.get(api_url, headers=(self.headers),
          params=params)

    def __get_api_url(self, api_specifics=''):
        model_name = 'calibration_constants/'
        return self.get_api_url(model_name, api_specifics)