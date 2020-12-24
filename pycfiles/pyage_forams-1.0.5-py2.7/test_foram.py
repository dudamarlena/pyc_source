# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyage_forams/solutions/test_foram.py
# Compiled at: 2014-10-11 19:21:41
from unittest import TestCase
from pyage.core import inject
from pyage_forams.solutions.foram import Foram

class TestForam(TestCase):

    def test_step(self):
        inject.config = 'pyage_forams.conf.dummy_conf'
        foram = Foram(10)