# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/system/polaris.py
# Compiled at: 2019-10-03 13:30:51
import json, os, unittest
from total_scattering.reduction import TotalScatteringReduction
from total_scattering.isis.polaris.generate_input import generate_input_json, POLARIS_DIR
from tests import IN_TRAVIS
run_test = False

class PolarisTotalScatteringSystemTest(unittest.TestCase):

    @unittest.skipIf(IN_TRAVIS or not run_test, 'Do not run thest on build servers')
    def test_silicon(self):
        """
        Run polaris silicon data through total scattering script
        """
        generate_input_json()
        path = os.path.join(POLARIS_DIR, 'test_input.json')
        with open(path, 'r') as (handle):
            config = json.load(handle)
        actual = TotalScatteringReduction(config)
        self.assertEqual(actual.getNumberHistograms(), 5)
        self.assertEqual(actual.getTitle(), '10: Silicon 640b, 700MeV, chopper stopped')
        self.assertEqual(actual.getInstrument().getFullName(), 'POLARIS')


if __name__ == '__main__':
    unittest.main()