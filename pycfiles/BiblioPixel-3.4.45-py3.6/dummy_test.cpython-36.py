# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/test/bibliopixel/drivers/dummy_test.py
# Compiled at: 2019-08-11 12:22:47
# Size of source mod 2**32: 477 bytes
import argparse, time, unittest
from bibliopixel.layout.strip import Strip
from bibliopixel.drivers.dummy import Dummy
from bibliopixel.project import clock

def clock_only_project():
    return argparse.Namespace(clock=(clock.Clock()))


class DummyTest(unittest.TestCase):

    def test_dummy(self):
        for driver in (Dummy(32), Dummy(32, 0.01)):
            driver.set_project(clock_only_project())
            layout = Strip([driver])
            layout.push_to_driver()