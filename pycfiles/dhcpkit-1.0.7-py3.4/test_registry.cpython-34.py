# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/dhcpkit/tests/test_registry.py
# Compiled at: 2017-06-23 18:27:42
# Size of source mod 2**32: 4514 bytes
"""
Test whether the basic stuff of Registry works as intended
"""
import logging, unittest
from collections import OrderedDict
import pkg_resources
from dhcpkit.ipv6.options import ClientIdOption, ServerIdOption
from dhcpkit.registry import Registry

class TestRegistry(Registry):
    __doc__ = "\n    A registry that doesn't exist to test with\n    "
    entry_point = 'dhcpkit.tests.registry'


class ElementOccurrenceTestCase(unittest.TestCase):

    def test_registry_loading(self):
        entry_map = pkg_resources.get_entry_map('dhcpkit')
        dist = entry_map['dhcpkit.ipv6.options']['1'].dist
        entry_map['dhcpkit.tests.registry'] = {'one': pkg_resources.EntryPoint.parse('one = dhcpkit.ipv6.options:ClientIdOption', dist=dist), 
         '1': pkg_resources.EntryPoint.parse('1 = dhcpkit.ipv6.options:ServerIdOption', dist=dist)}
        test_registry = TestRegistry()
        self.assertEqual(len(test_registry), 2)
        self.assertEqual(test_registry['one'], ClientIdOption)
        self.assertEqual(test_registry[1], ServerIdOption)

    def test_duplicate_entries(self):
        entry_map = pkg_resources.get_entry_map('dhcpkit')
        dist = entry_map['dhcpkit.ipv6.options']['1'].dist
        entry_map['dhcpkit.tests.registry'] = OrderedDict()
        entry_map['dhcpkit.tests.registry']['1'] = pkg_resources.EntryPoint.parse('1 = dhcpkit.ipv6.options:ClientIdOption', dist=dist)
        entry_map['dhcpkit.tests.registry']['1 '] = pkg_resources.EntryPoint.parse('1 = dhcpkit.ipv6.options:ServerIdOption', dist=dist)
        with self.assertLogs('dhcpkit.registry', logging.WARNING) as (cm):
            test_registry = TestRegistry()
        self.assertEqual(len(cm.output), 1)
        self.assertRegex(cm.output[0], '^WARNING:.*:Multiple entry points found for TestRegistry 1')
        self.assertEqual(len(test_registry), 1)
        self.assertEqual(test_registry[1], ClientIdOption)

    def test_version_mismatch(self):
        entry_map = pkg_resources.get_entry_map('dhcpkit')

        class DummyProvider(pkg_resources.EmptyProvider):
            __doc__ = '\n            A dummy providers that gives a dummy dependency\n            '

            def has_metadata(self, name):
                """
                Claim we have requirements
                """
                if name == 'requires.txt':
                    return True

            def get_metadata_lines(self, name):
                """
                Fake requirements.txt
                """
                if name == 'requires.txt':
                    yield 'dhcpkit > 999.999'

        dist = pkg_resources.Distribution(project_name='dummy', location='/dummy', version='999.999.999', metadata=DummyProvider())
        entry_map['dhcpkit.tests.registry'] = {'bad': pkg_resources.EntryPoint.parse('bad = dhcpkit.tests.does_not_exist:DummyOption', dist=dist)}
        with self.assertLogs('dhcpkit.registry', logging.WARNING) as (cm):
            test_registry = TestRegistry()
        self.assertEqual(len(cm.output), 1)
        self.assertRegex(cm.output[0], '^CRITICAL:.*:Entry point bad .* is not compatible')
        self.assertEqual(len(test_registry), 0)

    def test_bad_entry(self):
        entry_map = pkg_resources.get_entry_map('dhcpkit')
        dist = entry_map['dhcpkit.ipv6.options']['1'].dist
        entry_map['dhcpkit.tests.registry'] = {'bad': pkg_resources.EntryPoint.parse('bad = dhcpkit.tests.does_not_exist:DummyOption', dist=dist)}
        with self.assertLogs('dhcpkit.registry', logging.WARNING) as (cm):
            test_registry = TestRegistry()
        self.assertEqual(len(cm.output), 1)
        self.assertRegex(cm.output[0], '^ERROR:.*:Entry point bad .* could not be loaded')
        self.assertEqual(len(test_registry), 0)


if __name__ == '__main__':
    unittest.main()