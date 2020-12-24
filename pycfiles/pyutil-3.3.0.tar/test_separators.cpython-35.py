# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/user/code/pyutil/pyutil/test/current/json_tests/test_separators.py
# Compiled at: 2019-06-26 11:58:00
# Size of source mod 2**32: 1022 bytes
import textwrap
from unittest import TestCase
from pyutil import jsonutil as json

class TestSeparators(TestCase):

    def test_separators(self):
        h = [
         [
          'blorpie'], ['whoops'], [], 'd-shtaeou', 'd-nthiouh', 'i-vhbjkhnth',
         {'nifty': 87}, {'field': 'yes', 'morefield': False}]
        expect = textwrap.dedent('        [\n          [\n            "blorpie"\n          ] ,\n          [\n            "whoops"\n          ] ,\n          [] ,\n          "d-shtaeou" ,\n          "d-nthiouh" ,\n          "i-vhbjkhnth" ,\n          {\n            "nifty" : 87\n          } ,\n          {\n            "field" : "yes" ,\n            "morefield" : false\n          }\n        ]')
        d1 = json.dumps(h)
        d2 = json.dumps(h, indent=2, sort_keys=True, separators=(' ,', ' : '))
        h1 = json.loads(d1)
        h2 = json.loads(d2)
        self.assertEqual(h1, h)
        self.assertEqual(h2, h)
        self.assertEqual(d2, expect)