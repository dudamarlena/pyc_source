# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\seishub\core\tests\test_core_zope_compatibility.py
# Compiled at: 2010-12-23 17:42:44
"""Test Interface implementation adopted from zope test suite. Interface and 
implements declaration is taken from seishub.core."""
import unittest
from zope.interface.exceptions import BrokenImplementation, Invalid
from zope.interface import implementedBy, providedBy, invariant
from zope.interface import directlyProvides, Attribute
from seishub.core.core import Interface, implements

class mytest(Interface):
    pass


class C(object):

    def m1(self, a, b):
        """return 1"""
        return 1

    def m2(self, a, b):
        """return 2"""
        return 2


class IC(Interface):

    def m1(a, b):
        """return 1"""
        pass

    def m2(a, b):
        """return 2"""
        pass


C.__implemented__ = IC

class I1(Interface):

    def ma():
        """blah"""
        pass


class I2(I1):
    pass


class I3(Interface):
    pass


class I4(Interface):
    pass


class A(I1.deferred()):
    implements(I1)


class B(object):
    implements(I2, I3)


class D(A, B):
    pass


class E(A, B):
    __implemented__ = (
     A.__implemented__, C.__implemented__)


class FooInterface(Interface):
    """ This is an Abstract Base Class """
    foobar = Attribute('fuzzed over beyond all recognition')

    def aMethod(foo, bar, bingo):
        """ This is aMethod """
        pass

    def anotherMethod(foo=6, bar='where you get sloshed', bingo=(1, 3)):
        """ This is anotherMethod """
        pass

    def wammy(zip, *argues):
        """ yadda yadda """
        pass

    def useless(**keywords):
        """ useless code is fun! """
        pass


class Foo(object):
    """ A concrete class """
    implements(FooInterface)
    foobar = 'yeah'

    def aMethod(self, foo, bar, bingo):
        """ This is aMethod """
        return 'barf!'

    def anotherMethod(self, foo=6, bar='where you get sloshed', bingo=(1, 3)):
        """ This is anotherMethod """
        return 'barf!'

    def wammy(self, zip, *argues):
        """ yadda yadda """
        return 'barf!'

    def useless(self, **keywords):
        """ useless code is fun! """
        return 'barf!'


foo_instance = Foo()

class Blah(object):
    pass


new = Interface.__class__
FunInterface = new('FunInterface')
BarInterface = new('BarInterface', [FunInterface])
BobInterface = new('BobInterface')
BazInterface = new('BazInterface', [BobInterface, BarInterface])

def ifFooThenBar(obj):
    if getattr(obj, 'foo', None) and not getattr(obj, 'bar', None):
        raise Invalid('If Foo, then Bar!')
    return


class IInvariant(Interface):
    foo = Attribute('foo')
    bar = Attribute('bar; must eval to Boolean True if foo does')
    invariant(ifFooThenBar)


def BarGreaterThanFoo(obj):
    foo = getattr(obj, 'foo', None)
    bar = getattr(obj, 'bar', None)
    if foo is not None and isinstance(foo, type(bar)):
        if not bar > foo:
            raise Invalid('Please, Boo MUST be greater than Foo!')
    return


class ISubInvariant(IInvariant):
    invariant(BarGreaterThanFoo)


class InvariantC(object):
    pass


class ZopeCompatibilityTestCase(unittest.TestCase):

    def testInterfaceSetOnAttributes(self):
        self.assertEqual(FooInterface['foobar'].interface, FooInterface)
        self.assertEqual(FooInterface['aMethod'].interface, FooInterface)

    def testClassImplements(self):
        self.assert_(IC.implementedBy(C))
        self.assert_(I1.implementedBy(A))
        self.assert_(I1.implementedBy(B))
        self.assert_(not I1.implementedBy(C))
        self.assert_(I1.implementedBy(D))
        self.assert_(I1.implementedBy(E))
        self.assert_(not I2.implementedBy(A))
        self.assert_(I2.implementedBy(B))
        self.assert_(not I2.implementedBy(C))
        self.assert_(not I2.implementedBy(E))

    def testUtil(self):
        self.assert_(IC in implementedBy(C))
        self.assert_(I1 in implementedBy(A))
        self.assert_(I1 not in implementedBy(C))
        self.assert_(I2 in implementedBy(B))
        self.assert_(I2 not in implementedBy(C))
        self.assert_(IC in providedBy(C()))
        self.assert_(I1 in providedBy(A()))
        self.assert_(I1 not in providedBy(C()))
        self.assert_(I2 in providedBy(B()))
        self.assert_(I2 not in providedBy(C()))

    def testObjectImplements(self):
        self.assert_(IC.providedBy(C()))
        self.assert_(I1.providedBy(A()))
        self.assert_(I1.providedBy(B()))
        self.assert_(not I1.providedBy(C()))
        self.assert_(I1.providedBy(D()))
        self.assert_(I1.providedBy(E()))
        self.assert_(not I2.providedBy(A()))
        self.assert_(I2.providedBy(B()))
        self.assert_(not I2.providedBy(C()))
        self.assert_(not I2.providedBy(E()))

    def testDeferredClass(self):
        a = A()
        self.assertRaises(BrokenImplementation, a.ma)

    def testInterfaceExtendsInterface(self):
        self.assert_(BazInterface.extends(BobInterface))
        self.assert_(BazInterface.extends(BarInterface))
        self.assert_(BazInterface.extends(FunInterface))
        self.assert_(not BobInterface.extends(FunInterface))
        self.assert_(not BobInterface.extends(BarInterface))
        self.assert_(BarInterface.extends(FunInterface))
        self.assert_(not BarInterface.extends(BazInterface))

    def testVerifyImplementation(self):
        from zope.interface.verify import verifyClass
        self.assert_(verifyClass(FooInterface, Foo))
        self.assert_(Interface.providedBy(I1))

    def test_names(self):
        names = list(_I2.names())
        names.sort()
        self.assertEqual(names, ['f21', 'f22', 'f23'])
        names = list(_I2.names(all=True))
        names.sort()
        self.assertEqual(names, ['a1', 'f11', 'f12', 'f21', 'f22', 'f23'])

    def test_namesAndDescriptions(self):
        names = [ nd[0] for nd in _I2.namesAndDescriptions() ]
        names.sort()
        self.assertEqual(names, ['f21', 'f22', 'f23'])
        names = [ nd[0] for nd in _I2.namesAndDescriptions(1) ]
        names.sort()
        self.assertEqual(names, ['a1', 'f11', 'f12', 'f21', 'f22', 'f23'])
        for name, d in _I2.namesAndDescriptions(1):
            self.assertEqual(name, d.__name__)

    def test_getDescriptionFor(self):
        self.assertEqual(_I2.getDescriptionFor('f11').__name__, 'f11')
        self.assertEqual(_I2.getDescriptionFor('f22').__name__, 'f22')
        self.assertEqual(_I2.queryDescriptionFor('f33', self), self)
        self.assertRaises(KeyError, _I2.getDescriptionFor, 'f33')

    def test___getitem__(self):
        self.assertEqual(_I2['f11'].__name__, 'f11')
        self.assertEqual(_I2['f22'].__name__, 'f22')
        self.assertEqual(_I2.get('f33', self), self)
        self.assertRaises(KeyError, _I2.__getitem__, 'f33')

    def test___contains__(self):
        self.failUnless('f11' in _I2)
        self.failIf('f33' in _I2)

    def test___iter__(self):
        names = list(iter(_I2))
        names.sort()
        self.assertEqual(names, ['a1', 'f11', 'f12', 'f21', 'f22', 'f23'])

    def testAttr(self):
        description = _I2.getDescriptionFor('a1')
        self.assertEqual(description.__name__, 'a1')
        self.assertEqual(description.__doc__, 'This is an attribute')

    def testFunctionAttributes(self):
        meth = _I1['f12']
        self.assertEqual(meth.getTaggedValue('optional'), 1)

    def testInvariant(self):
        o = InvariantC()
        directlyProvides(o, IInvariant)

        def errorsEqual(self, o, error_len, error_msgs, interface=None):
            if interface is None:
                interface = IInvariant
            self.assertRaises(Invalid, interface.validateInvariants, o)
            e = []
            try:
                interface.validateInvariants(o, e)
            except Invalid as error:
                self.assertEquals(error.args[0], e)
            else:
                self._assert(0)

            self.assertEquals(len(e), error_len)
            msgs = [ error.args[0] for error in e ]
            msgs.sort()
            for msg in msgs:
                self.assertEquals(msg, error_msgs.pop(0))

            return

        self.assertEquals(IInvariant.getTaggedValue('invariants'), [
         ifFooThenBar])
        self.assertEquals(IInvariant.validateInvariants(o), None)
        o.bar = 27
        self.assertEquals(IInvariant.validateInvariants(o), None)
        o.foo = 42
        self.assertEquals(IInvariant.validateInvariants(o), None)
        del o.bar
        errorsEqual(self, o, 1, ['If Foo, then Bar!'])
        self.assertEquals(ISubInvariant.getTaggedValue('invariants'), [
         BarGreaterThanFoo])
        o = InvariantC()
        directlyProvides(o, ISubInvariant)
        o.foo = 42
        errorsEqual(self, o, 1, ['If Foo, then Bar!'], ISubInvariant)
        o.foo = 2
        o.bar = 1
        errorsEqual(self, o, 1, ['Please, Boo MUST be greater than Foo!'], ISubInvariant)
        o.foo = 1
        o.bar = 0
        errorsEqual(self, o, 2, ['If Foo, then Bar!',
         'Please, Boo MUST be greater than Foo!'], ISubInvariant)
        o.foo = 1
        o.bar = 2
        self.assertEquals(IInvariant.validateInvariants(o), None)
        o = InvariantC()
        directlyProvides(o, IInvariant)
        o.foo = 42
        old_invariants = IInvariant.getTaggedValue('invariants')
        invariants = old_invariants[:]
        invariants.append(BarGreaterThanFoo)
        IInvariant.setTaggedValue('invariants', invariants)
        errorsEqual(self, o, 1, ['If Foo, then Bar!'])
        o.foo = 2
        o.bar = 1
        errorsEqual(self, o, 1, ['Please, Boo MUST be greater than Foo!'])
        o.foo = 1
        o.bar = 0
        errorsEqual(self, o, 2, ['If Foo, then Bar!',
         'Please, Boo MUST be greater than Foo!'])
        o.foo = 1
        o.bar = 2
        self.assertEquals(IInvariant.validateInvariants(o), None)
        IInvariant.setTaggedValue('invariants', old_invariants)
        return

    def testIssue228(self):

        class I(Interface):
            """xxx"""
            pass

        class Bad:
            __providedBy__ = None

        self.failUnlessRaises(AttributeError, I.providedBy, Bad)


class _I1(Interface):
    a1 = Attribute('This is an attribute')

    def f11():
        pass

    def f12():
        pass

    f12.optional = 1


class _I1_(_I1):
    pass


class _I1__(_I1_):
    pass


class _I2(_I1__):

    def f21():
        pass

    def f22():
        pass

    f23 = f22


def suite():
    return unittest.makeSuite(ZopeCompatibilityTestCase, 'test')


if __name__ == '__main__':
    unittest.main()