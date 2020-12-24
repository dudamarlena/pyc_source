# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/Products/GroupUserFolder/tests/testInterface.py
# Compiled at: 2008-05-20 04:51:55
__doc__ = '\n\n'
__version__ = '$Revision:  $'
__docformat__ = 'restructuredtext'
import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))
from Log import *
from Testing import ZopeTestCase
from Interface import Verify
import string

def flattenList(lst):
    """
    flattenList => transform a (deep) sequence into a simple sequence
    """
    ret = []
    if type(lst) not in (type(()), type([])):
        return (lst,)
    for item in lst:
        if type(item) in (type(()), type([])):
            ret.extend(flattenList(item))
        else:
            ret.append(item)

    return ret


def flattenInterfaces(lst):
    """
    flattenInterfaces => fetch interfaces and inherited ones
    """
    ret = []
    lst = flattenList(lst)
    for intf in lst:
        bases = intf.getBases()
        ret.extend(flattenInterfaces(bases))
        if intf not in ret:
            ret.append(intf)

    return ret


from Products.GroupUserFolder import GroupUserFolder, GRUFUser

class TestInterface(ZopeTestCase.ZopeTestCase):
    __module__ = __name__

    def test01Interfaces(self):
        """
        Test that interfaces are okay
        """
        ignore = getattr(self, 'ignore_interfaces', [])
        for klass in self.klasses:
            intfs = getattr(klass, '__implements__', None)
            self.failUnless(intfs, "'%s' class doesn't implement an interface!" % (klass.__name__,))
            intfs = flattenList(intfs)
            for intf in intfs:
                if intf in ignore:
                    continue
                self.failUnless(Verify.verifyClass(intf, klass), "'%s' class doesn't implement '%s' interface correctly." % (klass.__name__, intf.__name__))

        return

    def test02TestCaseCompletude(self):
        """
        Check that the test case is complete : each interface entry xxx must be associated
        to a test_xxx method in the test class.
        """
        not_defined = []
        tests = dir(self)
        count = 0
        ignore = getattr(self, 'ignore_interfaces', [])
        for klass in self.klasses:
            intfs = getattr(klass, '__implements__', None)
            self.failUnless(intfs, "'%s' class doesn't implement an interface!" % (klass.__name__,))
            intfs = flattenInterfaces(intfs)
            for intf in intfs:
                if intf in ignore:
                    continue
                for name in intf.names():
                    count += 1
                    if 'test_%s' % (name,) not in tests:
                        not_defined.append('%s.%s' % (klass.__name__, name))

        if not_defined:
            raise RuntimeError, '%d (over %d) MISSING TESTS:\n%s do not have a test associated.' % (len(not_defined), count, string.join(not_defined, ', '))
        return

    def test03ClassSecurityInfo(self):
        """
        This method tests that each and every method has a ClassSecurityInfo() declaration
        XXX This doesn't walk through inheritance :(
        """
        not_defined = []
        count = 0
        ignore = getattr(self, 'ignore_interfaces', [])
        for klass in self.klasses:
            dict = dir(klass)
            intfs = getattr(klass, '__implements__', None)
            self.failUnless(intfs, "'%s' class doesn't implement an interface!" % (klass.__name__,))
            intfs = flattenInterfaces(intfs)
            for intf in intfs:
                if intf in ignore:
                    continue
                for name in intf.names():
                    count += 1
                    if '%s__roles__' % (name,) not in dict:
                        not_defined.append('%s.%s' % (klass.__name__, name))

        if not_defined:
            raise RuntimeError, '%d (over %d) MISSING SECURITY DECLARATIONS:\n%s do not have a security declaration associated.' % (len(not_defined), count, string.join(not_defined, ', '))
        return


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    return suite


if __name__ == '__main__':
    framework()