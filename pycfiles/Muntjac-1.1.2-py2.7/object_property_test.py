# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/test/server/data/util/object_property_test.py
# Compiled at: 2013-04-04 15:36:37
from unittest import TestCase
from muntjac.data.util.object_property import ObjectProperty

class ObjectPropertyTest(TestCase):

    def setUp(self):
        TestCase.setUp(self)
        self._super1 = TestSuperClass('super1')
        self._sub1 = TestSubClass('sub1')

    def testSimple(self):
        prop1 = ObjectProperty(self._super1, TestSuperClass)
        self.assertEquals('super1', prop1.getValue().getName())
        prop1 = ObjectProperty(self._super1)
        self.assertEquals('super1', prop1.getValue().getName())
        prop2 = ObjectProperty(self._sub1, TestSubClass)
        self.assertEquals('Subclass: sub1', prop2.getValue().getName())
        prop2 = ObjectProperty(self._sub1)
        self.assertEquals('Subclass: sub1', prop2.getValue().getName())

    def testSetValueObjectSuper(self):
        prop = ObjectProperty(self._super1, TestSuperClass)
        self.assertEquals('super1', prop.getValue().getName())
        prop.setValue(TestSuperClass('super2'))
        self.assertEquals('super1', self._super1.getName())
        self.assertEquals('super2', prop.getValue().getName())

    def testSetValueObjectSub(self):
        prop = ObjectProperty(self._sub1, TestSubClass)
        self.assertEquals('Subclass: sub1', prop.getValue().getName())
        prop.setValue(TestSubClass('sub2'))
        self.assertEquals('Subclass: sub1', self._sub1.getName())
        self.assertEquals('Subclass: sub2', prop.getValue().getName())

    def testSetValueStringSuper(self):
        prop = ObjectProperty(self._super1, TestSuperClass)
        self.assertEquals('super1', prop.getValue().getName())
        prop.setValue('super2')
        self.assertEquals('super1', self._super1.getName())
        self.assertEquals('super2', prop.getValue().getName())

    def testSetValueStringSub(self):
        prop = ObjectProperty(self._sub1, TestSubClass)
        self.assertEquals('Subclass: sub1', prop.getValue().getName())
        prop.setValue('sub2')
        self.assertEquals('Subclass: sub1', self._sub1.getName())
        self.assertEquals('Subclass: sub2', prop.getValue().getName())

    def testMixedGenerics(self):
        prop = ObjectProperty(self._sub1)
        self.assertEquals('Subclass: sub1', prop.getValue().getName())
        self.assertEquals(prop.getType(), TestSubClass)
        prop.setValue('sub2')
        self.assertEquals('Subclass: sub2', prop.getValue().getName())


class TestSuperClass(object):

    def __init__(self, name):
        self._name = name

    def getName(self):
        return self._name

    def __str__(self):
        return self.getName()


class TestSubClass(TestSuperClass):

    def __init__(self, name):
        super(TestSubClass, self).__init__('Subclass: ' + name)