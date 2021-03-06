# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/anybox/buildbot/capability/tests/test_steps.py
# Compiled at: 2017-10-20 04:47:35
import unittest
from buildbot.process.buildstep import SUCCESS
from buildbot.process.properties import Properties
from ..steps import SetCapabilityProperties
from ..constants import CAPABILITY_PROP_FMT

class TestSetCapabilityProperties(unittest.TestCase):

    def setUp(self):
        self.step = SetCapabilityProperties('zecap', capability_version_prop='zecap_version')

        def fakelog(*a):
            self.log = a

        self.step.addCompleteLog = fakelog
        self.step.build = Properties()
        self.step_status = None

        def finished(status):
            self.step_status = status

        self.step.finished = finished
        return

    def test_description(self):
        step = SetCapabilityProperties('somecap', description='abc', descriptionDone='def', descriptionSuffix='ghi')
        self.assertEqual(step.description, ['abc'])
        self.assertEqual(step.descriptionDone, ['def'])
        self.assertEqual(step.descriptionSuffix, ['ghi'])

    def test_one_avail_version(self):
        step = self.step
        step.setProperty('capability', dict(zecap={'1.0': dict(bin='/usr/bin/zecap')}), 'BuildSlave')
        step.start()
        self.assertEqual(self.step_status, SUCCESS)
        self.assertEqual(step.getProperty(CAPABILITY_PROP_FMT % ('zecap', 'bin')), '/usr/bin/zecap')

    def test_no_details(self):
        step = self.step
        step.setProperty('capability', dict(zecap={}), 'BuildSlave')
        step.start()
        self.assertEqual(self.step_status, SUCCESS)

    def test_requirement_other_cap(self):
        step = self.step
        step.setProperty('capability', dict(zecap={'1.0': dict(bin='/usr/bin/zecap')}, othercap={'1.0': dict(bin='other')}), 'BuildSlave')
        step.setProperty('build_requires', ['othercap < 2'])
        step.start()
        self.assertEqual(self.step_status, SUCCESS)
        self.assertEqual(step.getProperty(CAPABILITY_PROP_FMT % ('zecap', 'bin')), '/usr/bin/zecap')

    def test_one_dispatched_version(self):
        step = self.step
        step.setProperty('capability', dict(zecap={'1.0': dict(bin='/usr/bin/zecap1'), '2.0': dict(bin='/usr/bin/zecap2')}), 'BuildSlave')
        step.setProperty('zecap_version', '2.0')
        step.start()
        self.assertEqual(self.step_status, SUCCESS)
        self.assertEqual(step.getProperty(CAPABILITY_PROP_FMT % ('zecap', 'bin')), '/usr/bin/zecap2')

    def test_one_meeting_requirements(self):
        step = self.step
        step.setProperty('capability', dict(zecap={'1.0': dict(bin='/usr/bin/zecap1'), '2.0': dict(bin='/usr/bin/zecap2')}), 'BuildSlave')
        step.setProperty('build_requires', ['zecap < 2'])
        step.start()
        self.assertEqual(self.step_status, SUCCESS)
        self.assertEqual(step.getProperty(CAPABILITY_PROP_FMT % ('zecap', 'bin')), '/usr/bin/zecap1')

    def test_several_meeting_requirements(self):
        step = self.step
        step.setProperty('capability', dict(zecap={'1.0': dict(bin='/usr/bin/zecap1'), '2.0': dict(bin='/usr/bin/zecap2')}), 'BuildSlave')
        step.setProperty('build_requires', ['zecap'])
        step.start()
        self.assertEqual(self.step_status, SUCCESS)
        prop_val = step.getProperty(CAPABILITY_PROP_FMT % ('zecap', 'bin'))
        self.assertTrue(prop_val in ('/usr/bin/zecap1', '/usr/bin/zecap2'))