# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/calibration_client/apis/condition_api.py
# Compiled at: 2019-08-02 11:48:19
# Size of source mod 2**32: 1314 bytes
"""ConditionApi module class"""
import json
from ..common.base import Base

class ConditionApi(Base):

    def get_possible_conditions(self, condition):
        api_url = self._ConditionApi__get_api_url('get_possible_conditions')
        self.check_session_token()
        return self.oauth_client.session.get(api_url, data=(json.dumps(condition)),
          headers=(self.headers))

    def get_expected_condition(self, condition):
        api_url = self._ConditionApi__get_api_url('get_expected_condition')
        self.check_session_token()
        return self.oauth_client.session.get(api_url, data=(json.dumps(condition)),
          headers=(self.headers))

    def set_expected_condition(self, condition):
        api_url = self._ConditionApi__get_api_url('set_expected_condition')
        self.check_session_token()
        return self.oauth_client.session.post(api_url, data=(json.dumps(condition)),
          headers=(self.headers))

    def __get_api_url(self, api_specifics=''):
        model_name = 'conditions/'
        return self.get_api_url(model_name, api_specifics)