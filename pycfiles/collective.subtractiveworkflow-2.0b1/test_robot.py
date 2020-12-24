# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /media/psf/Home/Code/koodaamo/collective.subsitebehaviors/src/collective/subsitebehaviors/tests/test_robot.py
# Compiled at: 2015-02-05 07:04:58
from collective.subsitebehaviors.testing import ACCEPTANCE
from plone.testing import layered
import os, robotsuite, unittest

def test_suite():
    suite = unittest.TestSuite()
    current_dir = os.path.abspath(os.path.dirname(__file__))
    robot_dir = os.path.join(current_dir, 'robot')
    robot_tests = [ os.path.join('robot', doc) for doc in os.listdir(robot_dir) if doc.endswith('.robot') and doc.startswith('test_')
                  ]
    for test in robot_tests:
        suite.addTests([
         layered(robotsuite.RobotTestSuite(test), layer=ACCEPTANCE)])

    return suite