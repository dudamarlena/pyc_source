# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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