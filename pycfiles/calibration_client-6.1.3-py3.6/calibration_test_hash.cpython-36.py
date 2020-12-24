# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/calibration_client/tests/calibration_test_hash.py
# Compiled at: 2019-08-05 17:28:52
# Size of source mod 2**32: 8543 bytes
"""
This class is a Singleton created to allow us to access the current value
of the Calibration Hash used to test our code from any class and test instance.

That's necessary since we can only successfully retrieve a Calibration
Constant Version if the same was injected to the repository (Database)
"""
import logging
from datetime import datetime, timedelta
from pytz import timezone
__all__ = [
 'CalibrationTestHash']

class _CalibrationTestHash(object):

    def __init__(self, desired_begin_at=None):
        self.desired_begin_at = desired_begin_at
        self.valid_01 = _CalibrationTestHash._build_valid_test_hash_01(desired_begin_at)
        self.valid_search_01 = _CalibrationTestHash._build_valid_test_hash_02(desired_begin_at)

    @staticmethod
    def _build_valid_test_hash_01(desired_begin_at):
        logging.error('>' * 200 + ' _build_valid_test_hash_01 - INJECT')
        ccv_valid_dt = _CalibrationTestHash._gen_valid_ccv_datetime(desired_begin_at)
        valid_01_h = {'karabo_h':_CalibrationTestHash._build_valid_hash(ccv_valid_dt, 'inject'), 
         'begin_validity_at_exp':ccv_valid_dt['begin_validity_at_exp'], 
         'end_validity_at_exp':ccv_valid_dt['end_validity_at_exp'], 
         'begin_at_exp':ccv_valid_dt['begin_at_exp']}
        return valid_01_h

    @staticmethod
    def _build_valid_test_hash_02(desired_begin_at):
        logging.error('>' * 200 + ' _build_valid_test_hash_02 - SEARCH')
        if desired_begin_at is None:
            desired_begin_at = '2016-10-11T17:57:19.757000'
        ccv_valid_dt = _CalibrationTestHash._gen_valid_ccv_datetime(desired_begin_at)
        valid_02_h = {'karabo_h':_CalibrationTestHash._build_valid_hash(ccv_valid_dt, 'search'), 
         'begin_validity_at_exp':ccv_valid_dt['begin_validity_at_exp'], 
         'end_validity_at_exp':ccv_valid_dt['end_validity_at_exp'], 
         'begin_at_exp':ccv_valid_dt['begin_at_exp']}
        return valid_02_h

    @staticmethod
    def _loc(datetime_at, tz_str='Europe/Berlin'):
        tz = timezone(tz_str)
        datetime_at_tz = tz.localize(datetime_at)
        formatted_date_at = datetime_at_tz.isoformat()[:-13] + '.000'
        formatted_tz = datetime_at_tz.isoformat()[-6:]
        formatted_date_at = '{0}{1}'.format(formatted_date_at, formatted_tz)
        return formatted_date_at

    @staticmethod
    def _gen_valid_ccv_datetime(desired_begin_at):
        begin_validity_at = '2013-10-17T00:52:41+03:00'
        begin_validity_at_exp = '2013-10-16T23:52:41.000+02:00'
        now = datetime.today()
        insert_begin_at = now + timedelta(hours=(-1))
        begin_at = _CalibrationTestHash._loc(insert_begin_at, 'Europe/Lisbon')
        if desired_begin_at is None:
            exp_begin_at = now
        else:
            exp_begin_at = datetime.strptime(desired_begin_at, '%Y-%m-%dT%H:%M:%S.%f')
        begin_at_exp = _CalibrationTestHash._loc(exp_begin_at)
        insert_end_validity_at = now + timedelta(hours=(-2), seconds=1)
        end_validity_at = _CalibrationTestHash._loc(insert_end_validity_at, 'Atlantic/Azores')
        exp_end_validity_at = now + timedelta(seconds=1)
        end_validity_at_exp = _CalibrationTestHash._loc(exp_end_validity_at)
        ccv_test_datetime_h = {'begin_validity_at':begin_validity_at, 
         'begin_validity_at_exp':begin_validity_at_exp, 
         'begin_at':begin_at, 
         'begin_at_exp':begin_at_exp, 
         'end_validity_at':end_validity_at, 
         'end_validity_at_exp':end_validity_at_exp}
        return ccv_test_datetime_h

    @staticmethod
    def _build_valid_hash(ccv_valid_dt, flg_mode):
        cc_name = 'test_inject_cc_unique_name'
        ccv_name = 'test_inject_name_{0}'.format(ccv_valid_dt['begin_at'])
        if flg_mode == 'inject':
            logging.error('>' * 200 + ' INJECT Mode')
            dev_name = 'PHYSICAL_DEVICE-2_DO_NOT_DELETE'
            dev_type_name = 'UNIT_TEST_DEVICE_TYPE-1_DO_NOT_DELETE'
            cal_name = 'CALIBRATION_TEST-1_DO_NOT_DELETE'
            param_1_val = 123.0
            param_2_val = 10.0
        else:
            if flg_mode == 'search':
                logging.error('>' * 200 + ' SEARCH Mode')
                dev_name = 'PHYSICAL_DEVICE-1_DO_NOT_DELETE'
                dev_type_name = 'UNIT_TEST_DEVICE_TYPE-1_DO_NOT_DELETE'
                cal_name = 'CALIBRATION_TEST-2_DO_NOT_DELETE'
                param_1_val = 2.9
                param_2_val = 1.3
            else:
                logging.error('>' * 200 + ' NOT INJECT/SEARCH Mode')
                dev_name = 'PHYSICAL_DEVICE-3_DO_NOT_DELETE'
                dev_type_name = 'UNIT_TEST_DEVICE_TYPE-3_DO_NOT_DELETE'
                cal_name = 'CALIBRATION_TEST-3_DO_NOT_DELETE'
                param_1_val = 300.0
                param_2_val = 600.0
        detector_condition_h = {'flg_available':1, 
         'description':'', 
         'parameters':[
          {'parameter_name':'PARAMETER_TEST-1_DO_NOT_DELETE', 
           'value':param_1_val, 
           'flg_logarithmic':0, 
           'lower_deviation_value':2, 
           'upper_deviation_value':1, 
           'flg_available':1, 
           'description':''},
          {'parameter_name':'PARAMETER_TEST-2_DO_NOT_DELETE', 
           'value':param_2_val, 
           'flg_logarithmic':0, 
           'lower_deviation_value':0.1, 
           'upper_deviation_value':0.05, 
           'flg_available':1, 
           'description':''}]}
        cc_h = {'name':cc_name, 
         'device_type_name':dev_type_name, 
         'calibration_name':cal_name, 
         'flg_available':1, 
         'flg_auto_approve':1, 
         'description':''}
        path_to_file = 'xfel/cal/{0}/{1}/'.format(dev_type_name, dev_name)
        ccv_h = {'name':ccv_name, 
         'device_name':dev_name, 
         'path_to_file':path_to_file, 
         'file_name':'test_01', 
         'flg_good_quality':1, 
         'begin_validity_at':ccv_valid_dt['begin_validity_at'], 
         'end_validity_at':ccv_valid_dt['end_validity_at'], 
         'begin_at':ccv_valid_dt['begin_at'], 
         'raw_data_location':'/somewhere', 
         'description':'', 
         'start_idx':0, 
         'end_idx':1, 
         'data_set_name':cc_h['calibration_name']}
        valid_dict = {'detector_condition':detector_condition_h, 
         'calibration_constant':cc_h, 
         'calibration_constant_version':ccv_h}
        return valid_dict


def init(desired_begin_at):
    global cal_test_hash
    cal_test_hash = _CalibrationTestHash(desired_begin_at)


def CalibrationTestHash(desired_begin_at):
    init(desired_begin_at)
    return cal_test_hash