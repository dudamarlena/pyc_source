# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/user/code/pyutil/pyutil/test/current/json_tests/test_dump.py
# Compiled at: 2019-06-26 11:58:00
# Size of source mod 2**32: 453 bytes
from unittest import TestCase
try:
    from cStringIO import StringIO
except ImportError:
    from io import StringIO

from pyutil import jsonutil as json

class TestDump(TestCase):

    def test_dump(self):
        sio = StringIO()
        json.dump({}, sio)
        self.assertEqual(sio.getvalue(), '{}')

    def test_dumps(self):
        self.assertEqual(json.dumps({}), '{}')