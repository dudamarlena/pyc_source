# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./build/lib/supervisor/tests/test_confecho.py
# Compiled at: 2019-04-05 17:19:18
# Size of source mod 2**32: 549 bytes
"""Test suite for supervisor.confecho"""
import sys, unittest
from supervisor.compat import StringIO
from supervisor import confecho

class TopLevelFunctionTests(unittest.TestCase):

    def test_main_writes_data_out_that_looks_like_a_config_file(self):
        sio = StringIO()
        confecho.main(out=sio)
        output = sio.getvalue()
        self.assertTrue('[supervisord]' in output)


def test_suite():
    return unittest.findTestCases(sys.modules[__name__])


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')