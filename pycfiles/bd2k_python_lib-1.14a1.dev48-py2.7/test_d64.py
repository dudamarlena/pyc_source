# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bd2k/util/test/test_d64.py
# Compiled at: 2018-05-03 13:55:55
from __future__ import absolute_import
from builtins import map
from builtins import range
from unittest import TestCase
from bd2k.util.d64 import standard as d64
import os

class TestD64(TestCase):

    def test(self):
        l = [ os.urandom(i) for i in range(1000) ]
        self.assertEqual(list(map(d64.decode, sorted(map(d64.encode, l)))), sorted(l))