# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hvelarde/collective/behavior.richpreview/src/collective/behavior/richpreview/tests/test_robot.py
# Compiled at: 2018-04-05 17:11:05
from collective.behavior.richpreview.testing import ROBOT_TESTING
from plone.testing import layered
import os, robotsuite, unittest

def test_suite():
    suite = unittest.TestSuite()
    current_dir = os.path.abspath(os.path.dirname(__file__))
    tests = [ doc for doc in os.listdir(current_dir) if doc.startswith('test_') and doc.endswith('.robot')
            ]
    suite.addTests([ layered(robotsuite.RobotTestSuite(t), layer=ROBOT_TESTING) for t in tests
                   ])
    return suite