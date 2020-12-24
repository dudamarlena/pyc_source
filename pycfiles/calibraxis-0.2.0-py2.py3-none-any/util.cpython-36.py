# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/calibration_client/tests/common/util.py
# Compiled at: 2018-03-12 09:48:15
# Size of source mod 2**32: 4761 bytes
__doc__ = 'UtilTest Class with generic and util helper methods'
import json, unittest
from dateutil import parser
from .config_test import *

class Util(unittest.TestCase):

    @staticmethod
    def load_response_content(response):
        resp_str = response.content.decode('utf8')
        if resp_str == '':
            return {}
        else:
            return json.loads(resp_str)

    @staticmethod
    def debug_response(response):
        print('*' * 100)
        print('response.status_code =>', str(response.status_code))
        print('response.content =>', str(response.content))
        print('*' * 100)
        raise NameError('See response message content')

    def assert_eq_status_code(self, receive, expect):
        msg = "Validate 'status_code' value returned by server response: "
        compared_values_str = self._Util__get_comp_values(receive, expect)
        failure_msg = '{0}{1}'.format(msg, compared_values_str)
        self._Util__assert_eq_num(receive, expect, failure_msg, '')

    def assert_eq_str(self, receive, expect):
        msg = "Validate 'String' value returned by server response: "
        compared_values_str = self._Util__get_comp_values(receive, expect)
        failure_msg = '{0}{1}'.format(msg, compared_values_str)
        self._Util__assert_eq_str(receive, expect, failure_msg, 'info')

    def assert_eq_val(self, receive, expect):
        msg = "Validate 'Content' value returned by server response: "
        compared_values_str = self._Util__get_comp_values(receive, expect)
        failure_msg = '{0}{1}'.format(msg, compared_values_str)
        self._Util__assert_eq_flg(receive, expect, failure_msg, 'success')

    def assert_eq_hfield(self, receive, expect, field, field_typ, fail_msg=''):
        receive_field = receive[field]
        expect_field = expect[field]
        if field_typ.lower() == STRING:
            self._Util__assert_eq_str(receive_field, expect_field, fail_msg, field)
        else:
            if field_typ.lower() == NUMBER:
                self._Util__assert_eq_num(receive_field, expect_field, fail_msg, field)
            else:
                if field_typ.lower() == BOOLEAN:
                    self._Util__assert_eq_flg(receive_field, expect_field, fail_msg, field)
                else:
                    if field_typ.lower() == DATETIME:
                        self._Util__assert_eq_dt(receive_field, expect_field, fail_msg, field)
                    else:
                        self.assertEqual(1, 2, 'Specified field_type is not valid')

    def assert_not_eq_str(self, receive, expect, field):
        failure_msg = '{0} must be different'.format(field)
        self.assertNotEqual(receive, expect, failure_msg)

    def __assert_equal_internal(self, receive, expect, fail_msg, field, case_sensitive):
        if receive is None:
            receive = ''
        else:
            if expect is None:
                expect = ''
            assert_msg = self._Util__get_assert_msg(field, fail_msg, receive, expect)
            if case_sensitive:
                self.assertEqual(str(receive), str(expect), assert_msg)
            else:
                rec_lower_str = str(receive).lower()
                self.assertEqual(rec_lower_str, str(expect).lower(), assert_msg)

    def __get_assert_msg(self, field, fail_msg, receive, expect):
        assert_base_msg = self._Util__get_base_msg(field, fail_msg)
        compared_values_str = self._Util__get_comp_values(receive, expect)
        return '{0}{1}'.format(assert_base_msg, compared_values_str)

    def __get_base_msg(self, field, fail_msg):
        if fail_msg != '':
            return fail_msg
        else:
            return "Field '{0}' must be the same".format(field)

    def __get_comp_values(self, receive, expect):
        comp_msg = "(received: '{0}'; expected: '{1}')".format(receive, expect)
        return comp_msg

    def __assert_eq_str(self, receive, expect, fail_msg, field):
        self._Util__assert_equal_internal(receive, expect, fail_msg, field, case_sensitive=True)

    def __assert_eq_num(self, receive, expect, fail_msg, field):
        self._Util__assert_equal_internal(receive, expect, fail_msg, field, case_sensitive=False)

    def __assert_eq_flg(self, receive, expect, fail_msg, field):
        self._Util__assert_equal_internal(receive, expect, fail_msg, field, case_sensitive=False)

    def __assert_eq_dt(self, receive, expect, fail_msg, field):
        receive_dt = parser.parse(receive)
        expected_dt = parser.parse(expect)
        assert_msg = self._Util__get_assert_msg(field, fail_msg, receive, expect)
        self.assertEqual(receive_dt, expected_dt, assert_msg)