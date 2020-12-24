# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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