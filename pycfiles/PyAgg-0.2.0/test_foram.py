# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyage_forams/solutions/test_foram.py
# Compiled at: 2014-10-11 19:21:41
from unittest import TestCase
from pyage.core import inject
from pyage_forams.solutions.foram import Foram

class TestForam(TestCase):

    def test_step(self):
        inject.config = 'pyage_forams.conf.dummy_conf'
        foram = Foram(10)