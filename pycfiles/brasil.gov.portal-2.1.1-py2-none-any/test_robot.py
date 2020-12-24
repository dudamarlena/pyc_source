# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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