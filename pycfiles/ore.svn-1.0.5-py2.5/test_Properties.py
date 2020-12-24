# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/ore/svn/tests/test_Properties.py
# Compiled at: 2008-04-15 01:26:21
"""
$Id: test_Properties.py 1628 2006-09-03 02:13:48Z hazmat $
"""
from unittest import TestSuite, makeSuite, TestCase, main
from datetime import datetime
import time, os
from zope.interface import implements, Interface
from zope import schema
from ore.svn import SubversionContext
from ore.svn.property import NodePropertySheet
from ore.svn.interfaces import ISubversionProperties, IPropertySheet
from svn import core
from cPickle import dumps
from base64 import encodestring
from _base import SubversionTest

class IFoo(Interface):
    pass


class Bar(object):
    implements(IFoo)


class ITestSheet(Interface):
    foo = schema.Object(IFoo)


class TestSheet(NodePropertySheet):
    implements(ITestSheet)


TestSheet.setup2({'foo': ('object', 'foo')})

class TestSVNProperties(SubversionTest):

    def test_getPropertySheet(self):
        properties = ISubversionProperties(self.root['elephants.txt'])
        self.assertEqual(properties.externals, None)
        self.assertEqual(properties.executable, None)
        return

    def test_setPropertySheet(self):
        properties = ISubversionProperties(self.root['elephants.txt'])
        properties.executable = 'true'
        self.assertEqual(properties.executable, 'true')
        properties.mime_type = 'text/plain'
        self.assertEqual(properties.mime_type, 'text/plain')

    def test_PropertyMapping(self):
        node = self.root['elephants.txt']
        node.properties[core.SVN_PROP_MIME_TYPE] = 'text/plain'
        value = node.properties[core.SVN_PROP_MIME_TYPE]
        value2 = node.getProperty(core.SVN_PROP_MIME_TYPE)
        self.assertEqual(value, value2)
        self.assertEqual(value, 'text/plain')
        del node.properties[core.SVN_PROP_MIME_TYPE]
        value = node.properties[core.SVN_PROP_MIME_TYPE]
        self.assertEqual(value, None)
        return

    def test_ObjectProperty(self):
        bar = Bar()
        bar.name = 'ralph'
        value = {'person': bar}
        sheet = TestSheet(self.root['elephants.txt'])
        sheet.foo = value
        self.assertEqual(encodestring(dumps(value)), self.root['elephants.txt'].getProperty('foo'))
        self.assertEqual(sheet.foo['person'].name, bar.name)


def test_suite():
    suite = TestSuite()
    suite.addTest(makeSuite(TestSVNProperties))
    return suite


if __name__ == '__main__':
    main()