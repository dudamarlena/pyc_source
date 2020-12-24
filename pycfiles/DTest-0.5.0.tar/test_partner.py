# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/klmitch/devel/src/dtest/tests/test_partner.py
# Compiled at: 2011-04-12 12:15:32
from dtest import *
from dtest.util import *
setUpRun = False
tearDownRun = False

def setUp():
    global setUpRun
    setUpRun = True


def tearDown():
    global tearDownRun
    tearDownRun = True