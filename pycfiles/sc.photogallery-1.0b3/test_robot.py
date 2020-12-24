# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hvelarde/collective/sc.photogallery/src/sc/photogallery/tests/test_robot.py
# Compiled at: 2017-10-20 20:11:12
from plone.testing import layered
from sc.photogallery.testing import IS_PLONE_5
from sc.photogallery.testing import ROBOT_TESTING
import os, robotsuite, unittest
dirname = os.path.dirname(__file__)
files = os.listdir(dirname)
tests = [ f for f in files if f.startswith('test_') and f.endswith('.robot') ]
if IS_PLONE_5:
    tests = []

def test_suite():
    suite = unittest.TestSuite()
    suite.addTests([ layered(robotsuite.RobotTestSuite(t, noncritical=['Expected Failure']), layer=ROBOT_TESTING) for t in tests
                   ])
    return suite