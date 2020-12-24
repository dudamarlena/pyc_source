# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bika/health/tests/test_robot.py
# Compiled at: 2014-12-12 07:13:54
from bika.health.testing import HEALTH_ROBOT_TESTING
from plone.testing import layered
import robotsuite, unittest
ROBOT_TESTS = [
 'test_regulatoryinspector.robot']

def test_suite():
    suite = unittest.TestSuite()
    for RT in ROBOT_TESTS:
        suite.addTests([
         layered(robotsuite.RobotTestSuite(RT), layer=HEALTH_ROBOT_TESTING)])

    return suite