# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/tests/db/connector_test.py
# Compiled at: 2019-08-25 22:19:11
# Size of source mod 2**32: 265 bytes
from unittest import TestCase, skipUnless, skipIf
import pytest
from tests import online

@online
class ConnectionTest(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_something_real_quick(self):
        pass