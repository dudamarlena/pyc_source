# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3392)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/hvelarde/collective/lazysizes/src/collective/lazysizes/tests/test_robot.py
# Compiled at: 2016-10-22 10:15:51
# Size of source mod 2**32: 536 bytes
from collective.lazysizes.testing import ROBOT_TESTING
from plone.testing import layered
import os, robotsuite, unittest

def test_suite():
    suite = unittest.TestSuite()
    current_dir = os.path.abspath(os.path.dirname(__file__))
    tests = [doc for doc in os.listdir(current_dir) if doc.startswith('test_') if doc.endswith('.robot')]
    suite.addTests([layered((robotsuite.RobotTestSuite(t)), layer=ROBOT_TESTING) for t in tests])
    return suite