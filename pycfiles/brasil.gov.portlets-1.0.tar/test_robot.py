# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/hvelarde/forcontent/idg/src/brasil.gov.portal/src/brasil/gov/portal/tests/test_robot.py
# Compiled at: 2018-06-11 09:46:53
from brasil.gov.portal.testing import ACCEPTANCE_TESTING
from plone.testing import layered
import os, robotsuite, unittest
noncritical = [
 'Expected Failure']

def test_suite():
    suite = unittest.TestSuite()
    current_dir = os.path.abspath(os.path.dirname(__file__))
    robot_dir = os.path.join(current_dir, 'robot')
    tests = [ os.path.join('robot', doc) for doc in os.listdir(robot_dir) if doc.endswith('.robot') and doc.startswith('test_') and 'acessibilidade' not in doc
            ]
    for test in tests:
        suite.addTests([
         layered(robotsuite.RobotTestSuite(test, noncritical=noncritical), layer=ACCEPTANCE_TESTING)])

    return suite