# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mounts/isilon/data/eahome/q804348/ea_code/STAR-SEQR/starseqr_utils/tests/test_readsupport.py
# Compiled at: 2017-12-07 17:16:01
import unittest, os, sys
sys.path.insert(0, '../')
import starseqr_utils as su
path = os.path.dirname(__file__)
if path != '':
    os.chdir(path)

class ReadSupportTestCase(unittest.TestCase):
    """Tests read support"""

    def test_readsupport_v1(self):
        """v1"""
        pass


if __name__ == '__main__':
    unittest.main()