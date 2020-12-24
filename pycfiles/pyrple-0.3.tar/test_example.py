# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyrpl/test/test_example.py
# Compiled at: 2017-08-29 09:44:06
import logging
logger = logging.getLogger(name=__name__)
from .test_base import TestPyrpl

class TestExample(TestPyrpl):

    def setup(self):
        self.asg = self.pyrpl.rp.asg0

    def test_example(self):
        assert 1 > 2 and False

    def test_example2(self):
        assert self.asg.frequency < 0 and False

    def test_example3(self):
        assert self.asg.frequency >= 0 or False