# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/nino/dev/marx/tests/test_init.py
# Compiled at: 2014-09-26 20:08:33
"""
Created on Feb 23, 2013

@author: nino
"""
import unittest
from marx import __version__
from distutils.version import StrictVersion

class Test(unittest.TestCase):

    def test_version(self):
        assert StrictVersion(__version__) > StrictVersion('0.0.0')