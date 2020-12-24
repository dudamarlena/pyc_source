# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/paula/testing/testing.py
# Compiled at: 2008-08-18 21:14:28
"""
"""
__author__ = 'Florian Friesdorf <flo@chaoflow.net>'
__docformat__ = 'plaintext'
import os, os.path, unittest
from zope.app.testing.functional import ZCMLLayer, FunctionalDocFileSuite
from zope.component import testing
from zope.testing import doctest
from zope.testing import doctestunit
from UserDict import UserDict
from UserList import UserList
from zope.component import provideAdapter, provideUtility
from zope.component import adapts
from zope.component import getUtility, queryUtility
from zope.component import getSiteManager
from zope.interface import alsoProvides, implements, providedBy
from zope.interface import Interface, Attribute
from paula.testing import interact

class Mock(object):
    """a mock object that carries desired interfaces

        >>> class IA(Interface):
        ...     pass

        >>> class IB(Interface):
        ...     pass

        >>> m = Mock( a = 1, f = lambda : 2, alsoProvides=(IA,IB))
        >>> m.a
        1
        >>> m.f()
        2
        >>> IA.providedBy(m)
        True
    """
    __module__ = __name__
    implements(Interface)

    def __init__(self, **kwargs):
        if kwargs.has_key('alsoProvides'):
            alsoProvides(self, *kwargs['alsoProvides'])
            del kwargs['alsoProvides']
        for (k, v) in kwargs.items():
            setattr(self, k, v)


test_globs = dict(Attribute=Attribute, Interface=Interface, Mock=Mock, UserDict=UserDict, UserList=UserList, adapts=adapts, alsoProvides=alsoProvides, getUtility=getUtility, getSiteManager=getSiteManager, interact=interact.interact, implements=implements, provideAdapter=provideAdapter, provideUtility=provideUtility, providedBy=providedBy, queryUtility=queryUtility)

def setUp(test):
    """We can use this to set up anything that needs to be available for
    each test. It is run before each test, i.e. for each docstring that
    contains doctests.
    
    Look at the Python unittest and doctest module documentation to learn 
    more about how to prepare state and pass it into various tests.

        >>> m = Mock()
        >>> class IA(Interface):
        ...     pass

        >>> alsoProvides(m, IA)
        >>> providedBy(m) is not None
        True

        >>> provideUtility(m, IA)

        >>> class A(object):
        ...     adapts(Interface)
        ...     implements(IA)

        >>> provideAdapter(A)
    """
    testing.setUp(test)
    for (k, v) in test_globs.items():
        test.globs[k] = v


def tearDown(test):
    """
    """
    testing.tearDown(test)


def my_import(name):
    mod = __import__(name)
    components = name.split('.')
    for x in components[1:]:
        mod = getattr(mod, x)

    return mod


def recurse(*args):
    """returns all modules, that contain doctests

    returns all doctests found within the modules passed in *args

    For paula.testing itself, recurse should find 8 modules containing tests:

        >>> to_test = recurse('paula.testing')
        >>> len(to_test)
        9
    """
    result = []
    for name in args:
        mod = my_import(name)
        result += [mod]
        modname = mod.__file__.replace('.pyc', '').replace('.py', '')
        if modname.endswith('__init__'):
            dirname = os.path.dirname(mod.__file__)
            dirlist = os.listdir(dirname)
            for x in dirlist:
                fullpath = os.path.join(dirname, x)
                if not (os.path.isdir(fullpath) or x.endswith('.py')):
                    continue
                if os.path.isdir(fullpath) and not os.path.isfile(os.path.join(fullpath, '__init__.py')):
                    continue
                x = x.replace('.py', '')
                if x.startswith('.'):
                    continue
                if x == '__init__':
                    continue
                if x == 'tests':
                    continue
                mod_name = '%s.%s' % (name, x)
                result += recurse(mod_name)

    return result


def get_test_suite(pkg_name, tests=[]):
    """construct a test suite for a package
    
    recurses through a package and returns a test suite consisting of all
    doctest found + the tests passed as argument
    """

    def test_suite():
        to_test = recurse(pkg_name)
        optionflags = doctest.REPORT_ONLY_FIRST_FAILURE + doctest.ELLIPSIS + doctest.NORMALIZE_WHITESPACE
        unit_tests = []
        for x in to_test:
            unit_test = doctestunit.DocTestSuite(x, setUp=setUp, tearDown=tearDown, optionflags=optionflags)
            unit_tests.append(unit_test)

        test_suite = unittest.TestSuite(unit_tests + tests)
        return test_suite

    return test_suite


class SuiteGenerator(object):
    """
    """
    __module__ = __name__

    def __init__(self, package_name):
        self.package_name = package_name
        self.package = my_import(package_name)
        self.package_dir = os.path.dirname(self.package.__file__)
        self.ftesting_zcml = os.path.join(self.package_dir, 'ftesting.zcml')
        try:
            self.FunctionalLayer = ZCMLLayer(self.ftesting_zcml, package_name, 'FunctionalLayer', allow_teardown=True)
        except TypeError:
            self.FunctionalLayer = ZCMLLayer(self.ftesting_zcml, package_name, 'FunctionalLayer')

    @property
    def FunctionalDocFileSuite(self):

        def myFunctionalDocFileSuite(path, **kw):
            if 'package' not in kw:
                kw['package'] = self.package_name
            suite = FunctionalDocFileSuite(path, globs=test_globs, **kw)
            suite.layer = self.FunctionalLayer
            return suite

        return myFunctionalDocFileSuite