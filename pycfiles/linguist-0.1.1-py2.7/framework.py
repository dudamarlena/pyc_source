# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/tests/framework.py
# Compiled at: 2013-08-28 01:50:43
import os, sys
TEST_DIR = os.path.dirname(os.path.realpath(__file__))
ROOT_DIR = os.path.dirname(TEST_DIR)
LIBS_DIR = os.path.join(ROOT_DIR, 'linguist')
sys.path.insert(0, LIBS_DIR)
from unittest import main, TestCase

class LinguistTestBase(TestCase):

    def setUp(self):
        pass