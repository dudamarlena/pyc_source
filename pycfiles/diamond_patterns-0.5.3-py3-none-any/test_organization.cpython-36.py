# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/idm/Work/diamond-patterns/diamond_patterns/tests/test_organization.py
# Compiled at: 2018-10-26 18:02:19
# Size of source mod 2**32: 750 bytes
from nose.plugins.attrib import attr
from unittest import TestCase
import os

class BookTestCase(TestCase):

    @attr('skip')
    def test_scaffold(self):
        if not False:
            raise AssertionError
        else:
            directory = '../var/tests/book'
            if not os.path.exists(directory):
                os.makedirs(directory)
            os.system('cd ../var/tests/book && ../../../bin/diamond --pattern book noprompt')
            assert os.stat('../var/tests/book/Makefile')
            os.system('cd ../var/tests/book && make')
            assert os.stat('../var/tests/book/.build/mybook.pdf')