# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/errr/programs/python/gotland/tests/__init__.py
# Compiled at: 2014-09-29 23:50:44
# Size of source mod 2**32: 1192 bytes
import logging, os, sys
if sys.version_info < (2, 7):
    import unittest2 as unittest
else:
    import unittest

def tests_resource_path(local_path=''):
    this_file = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(this_file, local_path)


fixtures_path = tests_resource_path(local_path='fixtures')

class VCRBasedTests(unittest.TestCase):

    def setUp(self):
        logging.basicConfig()
        vcr_log = logging.getLogger('vcr')
        vcr_log.setLevel(logging.DEBUG)