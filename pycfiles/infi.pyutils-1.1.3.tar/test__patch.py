# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/Infinidat/infi.pyutils/tests/test__patch.py
# Compiled at: 2016-09-14 06:55:36
import os
from infi.pyutils.patch import patch
from .test_utils import TestCase

def listdir_patch(path):
    return [path]


TEST_PATH = '__infi_test'

class EnumTestCase(TestCase):

    def test__patch_context(self):
        with patch(os, 'listdir', listdir_patch):
            result = os.listdir(TEST_PATH)
            self.assertEqual(result, [TEST_PATH])
        self.assertNotEqual(os.listdir('.'), [TEST_PATH])