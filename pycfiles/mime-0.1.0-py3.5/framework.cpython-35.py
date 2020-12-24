# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/tests/framework.py
# Compiled at: 2016-08-03 22:31:30
# Size of source mod 2**32: 306 bytes
import os, sys
from unittest import TestCase
TEST_DIR = os.path.dirname(os.path.realpath(__file__))
ROOT_DIR = os.path.dirname(TEST_DIR)
LIBS_DIR = os.path.join(ROOT_DIR, 'mime')
sys.path.insert(0, LIBS_DIR)

class MIMETestBase(TestCase):

    def setUp(self):
        pass