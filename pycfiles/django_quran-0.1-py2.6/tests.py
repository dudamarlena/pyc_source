# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/quran/tests.py
# Compiled at: 2009-11-24 21:26:37
import doctest
from quran import buckwalter
from django.test import TestCase

class BuckwalterTest(TestCase):

    def test_buckwalter(self):
        """
        Test the buckwalter.py library.
        """
        doctest.testmod(buckwalter)