# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/errr/programs/python/thunderhead/tests/__init__.py
# Compiled at: 2014-11-27 16:23:30
import logging, os, sys
if sys.version_info < (2, 7):
    import unittest2 as unittest
else:
    import unittest
from thunderhead.connection import Connection
ADMIN_TOKEN = 'TOKSDVLMROYMFIYEDBLHXDHLPIV5IDYGHM2'
USER_TOKEN = 'TOKFWZWF5TO34NUREN5KETI2B1KESAC3HRZ'
CONNECTION = Connection(host='vusagemeter', token=ADMIN_TOKEN)

def tests_resource_path(local_path=''):
    this_file = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(this_file, local_path)


fixtures_path = tests_resource_path(local_path='fixtures')

class ThunderheadTests(unittest.TestCase):
    pass


class VCRBasedTests(unittest.TestCase):

    def setUp(self):
        logging.basicConfig()
        vcr_log = logging.getLogger('vcr')
        vcr_log.setLevel(logging.DEBUG)