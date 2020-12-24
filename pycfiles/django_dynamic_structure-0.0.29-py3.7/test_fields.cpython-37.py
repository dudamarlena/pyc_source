# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dyn_struct/tests/db/test_fields.py
# Compiled at: 2017-12-05 22:57:16
# Size of source mod 2**32: 466 bytes
from unittest import mock
from django.test import TestCase
from dyn_struct.db import fields

class ParamsFieldTest(TestCase):

    @mock.patch('dyn_struct.db.validators.ParamsValidator')
    def test_validators(self, mock_params):
        test_dict = {'test_key': 'test'}
        mock_params.return_value = test_dict
        params_field = fields.ParamsField()
        self.assertIn(test_dict, params_field.validators)
        self.assertTrue(mock_params.called)