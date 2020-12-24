# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/formskit/tests/test_errors.py
# Compiled at: 2015-07-25 09:04:48
# Size of source mod 2**32: 456 bytes
from formskit.tests.base import FormskitTestCase
from formskit import errors

class ErrorsTests(FormskitTestCase):

    def test_BadValue(self):
        error = errors.BadValue('name1')
        self.assertEqual('name1', error.name)
        self.assertEqual('name1', str(error))

    def test_ValueNotPresent(self):
        error = errors.ValueNotPresent('name2')
        self.assertEqual('name2', error.name)
        self.assertEqual('name2', str(error))