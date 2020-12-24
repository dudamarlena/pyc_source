# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/calibration_client/modules/calibration.py
# Compiled at: 2019-08-05 13:13:33
# Size of source mod 2**32: 3627 bytes
__doc__ = 'Calibration module class'
from ..apis.calibration_api import CalibrationApi
from ..common.base import Base
from ..common.config import *
MODULE_NAME = CALIBRATION

class Calibration(CalibrationApi):

    def __init__(self, calibration_client, name, unit_id, max_value, min_value, allowed_deviation, description=''):
        self.calibration_client = calibration_client
        self.id = None
        self.name = name
        self.unit_id = unit_id
        self.max_value = max_value
        self.min_value = min_value
        self.allowed_deviation = allowed_deviation
        self.description = description

    def create(self):
        cal_client = self.calibration_client
        response = cal_client.create_calibration_api(self._Calibration__get_resource())
        Base.cal_debug(MODULE_NAME, CREATE, response)
        res = Base.format_response(response, CREATE, CREATED, MODULE_NAME)
        if res['success']:
            self.id = res['data']['id']
        return res

    def delete(self):
        cal_client = self.calibration_client
        response = cal_client.delete_calibration_api(self.id)
        Base.cal_debug(MODULE_NAME, DELETE, response)
        return Base.format_response(response, DELETE, NO_CONTENT, MODULE_NAME)

    def update(self):
        cal_client = self.calibration_client
        response = cal_client.update_calibration_api(self.id, self._Calibration__get_resource())
        Base.cal_debug(MODULE_NAME, UPDATE, response)
        return Base.format_response(response, UPDATE, OK, MODULE_NAME)

    @staticmethod
    def get_by_id(cal_client, calibration_id):
        response = cal_client.get_calibration_by_id_api(calibration_id)
        Base.cal_debug(MODULE_NAME, 'get_by_id', response)
        return Base.format_response(response, GET, OK, MODULE_NAME)

    @staticmethod
    def get_all_by_name(cal_client, name):
        response = cal_client.get_all_calibrations_by_name_api(name)
        Base.cal_debug(MODULE_NAME, 'get_all_by_name', response)
        return Base.format_response(response, GET, OK, MODULE_NAME)

    @staticmethod
    def get_by_name(cal_client, name):
        res = Calibration.get_all_by_name(cal_client, name)
        if res['success']:
            if res['data'] == []:
                resp_data = []
            else:
                resp_data = res['data'][0]
            res = {'success':res['success'],  'info':res['info'], 
             'app_info':res['app_info'], 
             'data':resp_data}
        return res

    def __get_resource(self):
        calibration = {CALIBRATION: {'name':self.name, 
                       'unit_id':self.unit_id, 
                       'max_value':self.max_value, 
                       'min_value':self.min_value, 
                       'allowed_deviation':self.allowed_deviation, 
                       'description':self.description}}
        return calibration