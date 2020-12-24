# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/holmium/core/deprecated.py
# Compiled at: 2016-02-28 21:16:09
"""
aliases so that a real error message is displayed if someone
uses the old class named
"""
from .pageobject import Page, Element, Elements, ElementMap
from .testcase import TestCase

class Deprecated(object):
    """
    meta class to create an object that throws a Syntax error on
    construction
    """

    def __new__(cls, *_):
        raise SyntaxError('%s has been removed as of version 0.4. Use %s instead' % (
         cls.cur, cls.alt.__name__))


def construct_deprecated(name, alt):
    """
    create a type for the alias
    """
    doc = 'Deprecated alias for :class:`%s`' % alt.__name__
    cls = type(name, (Deprecated, alt), dict(cur=name, alt=alt, __doc__=doc))
    return cls


PageObject = construct_deprecated('PageObject', Page)
PageElement = construct_deprecated('PageElement', Element)
PageElements = construct_deprecated('PageElements', Elements)
PageElementMap = construct_deprecated('PageElementMap', ElementMap)
HolmiumTestCase = construct_deprecated('HolmiumTestCase', TestCase)