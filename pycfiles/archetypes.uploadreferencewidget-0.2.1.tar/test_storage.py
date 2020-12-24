# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/archetypes/schematuning/tests/test_storage.py
# Compiled at: 2010-01-22 07:59:46
__doc__ = '\n'
from Products.Archetypes.tests.attestcase import ATTestCase
from Products.Archetypes.atapi import *
from Products.Archetypes.tests.test_classgen import Dummy
from Products.Archetypes.tests.test_classgen import gen_dummy
from DateTime import DateTime
from archetypes.schematuning.tests.base import SchemaTuningTestCase

class ChangeStorageTest(SchemaTuningTestCase):
    __module__ = __name__

    def afterSetUp(self):
        gen_dummy()
        self._dummy = dummy = Dummy(oid='dummy')
        self._dummy.initializeArchetype()
        self._old_storages = {}

    def test_changestorage(self):
        dummy = self._dummy
        dummy.setAtextfield('sometext', mimetype='text/plain')
        dummy.setAdatefield('2003-01-01')
        dummy.setAlinesfield(['bla', 'bla', 'bla'])
        dummy.setAnobjectfield('someothertext')
        out = ('bla', 'bla', 'bla')
        self.failUnlessEqual(str(dummy.getAtextfield()), 'sometext')
        self.failUnlessEqual(dummy.getAdatefield(), DateTime('2003-01-01'))
        self.failUnlessEqual(dummy.getAlinesfield(), out)
        self.failUnlessEqual(dummy.getAnobjectfield(), 'someothertext')
        for field in dummy.schema.fields():
            if field.getName() in ['atextfield', 'adatefield', 'alinesfield', 'anobjectfield']:
                self._old_storages[field.getName()] = field.getStorage()
                field.setStorage(dummy, AttributeStorage())
                self.failUnlessEqual(field.getStorage().getName(), 'AttributeStorage')
                field.setStorage(dummy, MetadataStorage())
                self.failUnlessEqual(field.getStorage().getName(), 'MetadataStorage')

        dummy.invalidateSchema()
        self.failUnlessEqual(str(dummy.getAtextfield()), 'sometext')
        self.failUnlessEqual(dummy.getAdatefield(), DateTime('2003-01-01'))
        self.failUnlessEqual(dummy.getAlinesfield(), out)
        self.failUnlessEqual(dummy.getAnobjectfield(), 'someothertext')

    def test_unset(self):
        dummy = self._dummy
        dummy.setAtextfield('sometext')
        field = dummy.getField('atextfield')
        field.setStorage(dummy, AttributeStorage())
        self.failUnless(hasattr(dummy, 'atextfield'))
        field.setStorage(dummy, MetadataStorage())
        self.failIf(hasattr(dummy, 'atextfield'))
        self.failUnless(dummy._md.has_key('atextfield'))
        field.setStorage(dummy, AttributeStorage())
        self.failIf(dummy._md.has_key('atextfield'))
        self.failUnless(hasattr(dummy, 'atextfield'))


class MetadataStorageTest(ATTestCase):
    __module__ = __name__

    def afterSetUp(self):
        gen_dummy()
        self._dummy = dummy = Dummy(oid='dummy')
        self._dummy.initializeArchetype()
        for field in dummy.schema.fields():
            if field.getName() in ['atextfield', 'adatefield', 'alinesfield', 'anobjectfield']:
                field.setStorage(dummy, MetadataStorage())


class AttributeStorageTest(ATTestCase):
    __module__ = __name__

    def afterSetUp(self):
        gen_dummy()
        self._dummy = dummy = Dummy(oid='dummy')
        self._dummy.initializeArchetype()
        for field in dummy.schema.fields():
            if field.getName() in ['atextfield', 'adatefield', 'alinesfield', 'anobjectfield']:
                field.setStorage(dummy, AttributeStorage())


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(ChangeStorageTest))
    suite.addTest(makeSuite(MetadataStorageTest))
    suite.addTest(makeSuite(AttributeStorageTest))
    return suite