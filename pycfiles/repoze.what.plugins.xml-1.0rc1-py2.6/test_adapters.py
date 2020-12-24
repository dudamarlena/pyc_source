# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/tests/test_adapters.py
# Compiled at: 2009-01-27 15:55:31
"""The test suite for the adapters in the repoze.what XML plugin"""
import unittest, os
from shutil import copy
from repoze.what.adapters.testutil import GroupsAdapterTester, PermissionsAdapterTester
from repoze.what.plugins.xml import XMLGroupsAdapter, XMLPermissionsAdapter
here = os.path.abspath(os.path.dirname(__file__))
fixtures = os.path.join(here, 'fixture')

class _BaseXmlAdapterTester(unittest.TestCase):
    """The base test case for the XML source adapters"""

    def _setup_xml_adapter(self):
        tmp_filename = self.filename + '.tmp'
        original = os.path.join(fixtures, self.filename)
        self.tmp_file = os.path.join(fixtures, tmp_filename)
        copy(original, self.tmp_file)
        self.adapter = self.adapter_class(self.tmp_file)

    def tearDown(self):
        os.remove(self.tmp_file)

    def test_open_file_works(self):
        open_file = open(self.tmp_file, 'rw+')
        adapter = self.adapter_class(open_file)
        adapter.create_section('i_dont_exist')
        open_file.close()

    def test_file_really_is_updated(self):
        sections = self.adapter.get_all_sections()
        self.adapter.create_section('helloworld')
        sections['helloworld'] = set()
        new_adapter = self.adapter_class(self.tmp_file)
        self.assertEqual(sections, new_adapter.get_all_sections())

    def test_unicode_support(self):
        sections = self.adapter.get_all_sections()
        self.adapter.create_section('caraqueños')
        self.adapter.include_item('caraqueños', 'maría')


class TestXMLGroupsAdapter(GroupsAdapterTester, _BaseXmlAdapterTester):
    """Test case for the XML group source adapter"""
    filename = 'groups.xml'
    adapter_class = XMLGroupsAdapter

    def setUp(self):
        super(TestXMLGroupsAdapter, self).setUp()
        self._setup_xml_adapter()


class TestXMLPermissionsAdapter(PermissionsAdapterTester, _BaseXmlAdapterTester):
    """Test case for the XML permission source adapter"""
    filename = 'permissions.xml'
    adapter_class = XMLPermissionsAdapter

    def setUp(self):
        super(TestXMLPermissionsAdapter, self).setUp()
        self._setup_xml_adapter()