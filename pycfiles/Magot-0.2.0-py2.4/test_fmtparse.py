# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/magot/tests/test_fmtparse.py
# Compiled at: 2004-12-01 18:22:29
from unittest import TestCase, makeSuite, TestSuite
import unittest
from peak.api import *
from peak.tests import testRoot
from peak.util import fmtparse

class Thing(model.Element):
    __module__ = __name__

    class subexpr(model.Collection):
        __module__ = __name__
        referencedType = 'Thing'
        separator = ','
        lowerBound = 1

    mdl_syntax = fmtparse.Alternatives('X', fmtparse.Sequence('(', subexpr, ')'))


class Expression(model.Element):
    __module__ = __name__

    class terms(model.Collection):
        __module__ = __name__
        lowerBound = 1
        referencedType = 'Term'
        separator = '+'

    mdl_syntax = fmtparse.Sequence(terms)


class Term(model.Element):
    __module__ = __name__

    class factors(model.Collection):
        __module__ = __name__
        lowerBound = 1
        referencedType = 'Factor'
        separator = '*'

    mdl_syntax = fmtparse.Sequence(factors)


class Factor(model.Element):
    __module__ = __name__

    class constant(model.Attribute):
        __module__ = __name__
        referencedType = model.Integer

    class subexpr(model.Attribute):
        __module__ = __name__
        referencedType = Expression

    mdl_syntax = fmtparse.Alternatives(constant, fmtparse.Sequence('(', subexpr, ')'))


class XX(model.Element):
    __module__ = __name__

    class yy(model.Sequence):
        __module__ = __name__
        referencedType = model.Integer
        separator = ','


class parseFmtTest(TestCase):
    __module__ = __name__

    def test_SimpleParse(self):
        e = Thing.mdl_fromString('(X,((X)),(X,X,(X)))')
        str(e)
        e = Expression.mdl_fromString('1+2+3')
        assert len(e.terms) == 3

    def test_FeatureParse(self):
        self.assertEqual([1, 2, 3], XX.yy.parse('1,2,3'))

    def test_FeatureFormat(self):
        self.assertEqual('1,2,3', XX.yy.format([1, 2, 3]))


if __name__ == '__main__':
    unittest.main()