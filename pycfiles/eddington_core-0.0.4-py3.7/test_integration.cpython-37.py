# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/integration/test_integration.py
# Compiled at: 2020-04-04 11:50:41
# Size of source mod 2**32: 2332 bytes
import json
from pathlib import Path
from unittest import TestCase
import numpy as np
from eddington_core.fit_functions.fit_functions_registry import FitFunctionsRegistry
from eddington_core.fit_data import FitData
from integration.fitting_test_case import FitResultBaseTestCase, add_integration_tests

class TestFittingIntegration(TestCase):

    def compare_small(self, expected, actual, title, decimal):
        expected_copy = np.abs(expected)
        actual_copy = np.abs(actual)
        if expected_copy != 0:
            while expected_copy < 1:
                expected_copy *= 10
                actual_copy *= 10

        self.assertAlmostEqual(expected_copy,
          actual_copy,
          places=decimal,
          msg=f"{title} is different than expected. {expected} != {actual}")

    @classmethod
    def load_tests(cls):
        cases_path = Path(__file__).parent / 'cases'
        for json_path in cases_path.glob('**/*.json'):
            with open((str(json_path)), mode='r') as (json_file):
                json_obj = json.load(json_file)
            func_name = json_obj['fit_function']
            parameters = json_obj.get('parameters', [])
            func = (FitFunctionsRegistry.load)(func_name, *parameters)
            data_dict = json_obj['data']
            data = FitData(x=(np.array(data_dict['x'])),
              xerr=(np.array(data_dict['xerr'])),
              y=(np.array(data_dict['y'])),
              yerr=(np.array(data_dict['yerr'])))
            a0 = np.array(json_obj['a0'])
            decimal = json_obj.get('decimal', FitResultBaseTestCase.default_decimal)
            result = json_obj['result']
            case = FitResultBaseTestCase(name=(json_path.stem),
              func=func,
              data=data,
              a0=a0,
              a=(np.array(result['a'])),
              aerr=(np.array(result['aerr'])),
              arerr=(np.array(result['arerr'])),
              chi2=(result['chi2']),
              degrees_of_freedom=(result['degrees_of_freedom']),
              chi2_reduced=(result['chi2_reduced']),
              p_probability=(result['p_probability']),
              decimal=decimal)
            add_integration_tests(cls, case)


TestFittingIntegration.load_tests()