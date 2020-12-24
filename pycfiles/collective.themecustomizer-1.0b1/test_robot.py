# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hvelarde/collective/themecustomizer/src/collective/themecustomizer/tests/test_robot.py
# Compiled at: 2014-01-10 09:20:53
from collective.themecustomizer.testing import ROBOT_TESTING
from plone.testing import layered
import os, robotsuite, unittest
dirname = os.path.dirname(__file__)
files = os.listdir(dirname)
tests = [ f for f in files if f.startswith('test_') and f.endswith('.robot') ]

def test_suite():
    suite = unittest.TestSuite()
    suite.addTests([ layered(robotsuite.RobotTestSuite(t, noncritical=['Expected Failure']), layer=ROBOT_TESTING) for t in tests
                   ])
    return suite