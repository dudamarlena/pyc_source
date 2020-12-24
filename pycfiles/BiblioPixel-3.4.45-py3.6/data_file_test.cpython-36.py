# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/test/bibliopixel/util/data_file_test.py
# Compiled at: 2019-08-11 12:22:47
# Size of source mod 2**32: 1384 bytes
import unittest
from bibliopixel.util import data_file
DATA = "\ncontrols:\n    -\n        typename: midi\n\n        extractor:\n            accept:\n              type: control_change\n\n        routing:\n            00: animation.limit.ratio\n            01: animation.levels.knee\n            02: animation.levels.gain\n            09: animation.levels.enable  # yaml interprets this as a string '09'\n            10: animation.levels.ratio\n            020: animation.levels.knee   # yaml interprets this as octal\n"

class DataFileTest(unittest.TestCase):

    def test_yaml_keys(self):
        result = data_file.loads(DATA, 'test.yml')
        routing = result['controls'][0]['routing']
        self.assertEqual(routing['0'], 'animation.limit.ratio')
        self.assertEqual(set(routing), set(('0', '1', '2', '09', '10', '16')))
        self.assertEqual(data_file.loads(DATA, use_yaml=True), result)

    def test_round_trip_data_file(self):
        result = data_file.loads(DATA, 'test.yml')
        saved = data_file.dumps(result)
        restored = data_file.loads(saved)
        self.assertEqual(result, restored)

    def test_round_trip_yaml(self):
        result = data_file.loads(DATA, 'test.yml')
        saved = data_file.dumps(result, use_yaml=True)
        restored = data_file.loads(saved, use_yaml=True)
        self.assertEqual(result, restored)