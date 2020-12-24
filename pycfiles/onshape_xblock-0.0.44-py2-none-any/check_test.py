# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ethankeller/edx/xblock_development/onshape_xblock/onshape_xblock/checks/check_test.py
# Compiled at: 2019-05-10 10:14:00
from onshape_xblock.check_imports import *

class CheckTest(CheckBase):
    failure_message_template = ''

    def __init__(self, test_param='optional'):
        self.test_param = test_param
        super(CheckTest, self).__init__(name='Testing', onshape_element='https://cad.onshape.com/documents/cca81d10f239db0db9481e6f/v/ca51b7554314d6aab254d2e6/e/69c9eedda86512966b20bc90')

    def execute_check(self):
        pass