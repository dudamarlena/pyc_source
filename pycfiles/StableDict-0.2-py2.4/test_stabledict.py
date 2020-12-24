# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.freebsd-6.2-STABLE-i386/egg/test_stabledict.py
# Compiled at: 2007-08-28 04:31:41
from __future__ import generators
import random, unittest, warnings
from test import test_support
from stabledict import StableDict, _WRNnoOrderArg, _WRNnoOrderKW
import sys, UserDict, cStringIO
_EsizeChanged = "changing StableDict size during iteration doesn't raise Error"
_EmayLoopForever = 'StableDict iterator affected by mutations during iteration'
runningCPython = False
try:
    import os
    if os.name in ('posix', 'nt', 'mac', 'os2', 'ce', 'riscos'):
        runningCPython = True
except:
    pass

def needsCPython(*version):
    """Raise TestSkipped error when Python is older than version.

    Used to skip tests known to fail on older CPython versions."""
    if not runningCPython:
        return
    assert version
    if len(version) == 1 and isinstance(version[0], tuple):
        version = version[0]
    if sys.version_info < version:
        raise test_support.TestSkipped('known to fail on CPython < %r' % (version,))


class DictTest(unittest.TestCase):
    __module__ = __name__

    def test_constructor(self):
        self.assertEqual(StableDict(), StableDict())
        self.assert_(StableDict() is not StableDict())

    def test_bool(self):
        self.assert_(not StableDict())
        self.assert_({1: 2})
        self.assert_(bool(StableDict()) is False)
        self.assert_(bool({1: 2}) is True)

    def test_keys(self):
        d = StableDict()
        self.assertEqual(d.keys(), [])
        d = {'a': 1, 'b': 2}
        k = d.keys()
        self.assert_(d.has_key('a'))
        self.assert_(d.has_key('b'))
        self.assertRaises(TypeError, d.keys, None)
        return

    def test_values(self):
        d = StableDict()
        self.assertEqual(d.values(), [])
        d = {1: 2}
        self.assertEqual(d.values(), [2])
        self.assertRaises(TypeError, d.values, None)
        return

    def test_items(self):
        d = StableDict()
        self.assertEqual(d.items(), [])
        d = {1: 2}
        self.assertEqual(d.items(), [(1, 2)])
        self.assertRaises(TypeError, d.items, None)
        return

    def test_has_key(self):
        d = StableDict()
        self.assert_(not d.has_key('a'))
        d = {'a': 1, 'b': 2}
        k = d.keys()
        k.sort()
        self.assertEqual(k, ['a', 'b'])
        self.assertRaises(TypeError, d.has_key)

    def test_contains(self):
        d = StableDict()
        self.assert_('a' not in d)
        self.assert_('a' not in d)
        d = {'a': 1, 'b': 2}
        self.assert_('a' in d)
        self.assert_('b' in d)
        self.assert_('c' not in d)
        self.assertRaises(TypeError, d.__contains__)

    def test_len(self):
        d = StableDict()
        self.assertEqual(len(d), 0)
        d = {'a': 1, 'b': 2}
        self.assertEqual(len(d), 2)

    def test_getitem(self):
        d = {'a': 1, 'b': 2}
        self.assertEqual(d['a'], 1)
        self.assertEqual(d['b'], 2)
        d['c'] = 3
        d['a'] = 4
        self.assertEqual(d['c'], 3)
        self.assertEqual(d['a'], 4)
        del d['b']
        self.assertEqual(d, {'a': 4, 'c': 3})
        self.assertRaises(TypeError, d.__getitem__)

        class BadEq(object):
            __module__ = __name__

            def __eq__(self, other):
                raise Exc()

        d = StableDict()
        d[BadEq()] = 42
        self.assertRaises(KeyError, d.__getitem__, 23)

        class Exc(Exception):
            __module__ = __name__

        class BadHash(object):
            __module__ = __name__
            fail = False

            def __hash__(self):
                if self.fail:
                    raise Exc()
                else:
                    return 42

        d = StableDict()
        x = BadHash()
        d[x] = 42
        x.fail = True
        self.assertRaises(Exc, d.__getitem__, x)

    def test_clear(self):
        d = {1: 1, 2: 2, 3: 3}
        d.clear()
        self.assertEqual(d, StableDict())
        self.assertRaises(TypeError, d.clear, None)
        return

    def test_update(self):
        d = StableDict()
        d.update({1: 100})
        d.update({2: 20})
        d.update({1: 1, 2: 2, 3: 3})
        self.assertEqual(d, {1: 1, 2: 2, 3: 3})
        d.update()
        self.assertEqual(d, {1: 1, 2: 2, 3: 3})
        self.assertRaises((TypeError, AttributeError), d.update, None)

        class SimpleUserDict:
            __module__ = __name__

            def __init__(self):
                self.d = {1: 1, 2: 2, 3: 3}

            def keys(self):
                return self.d.keys()

            def __getitem__(self, i):
                return self.d[i]

        d.clear()
        d.update(SimpleUserDict())
        self.assertEqual(d, {1: 1, 2: 2, 3: 3})

        class Exc(Exception):
            __module__ = __name__

        d.clear()

        class FailingUserDict:
            __module__ = __name__

            def keys(self):
                raise Exc

        self.assertRaises(Exc, d.update, FailingUserDict())

        class FailingUserDict:
            __module__ = __name__

            def keys(self):

                class BogonIter:
                    __module__ = __name__

                    def __init__(self):
                        self.i = 1

                    def __iter__(self):
                        return self

                    def next(self):
                        if self.i:
                            self.i = 0
                            return 'a'
                        raise Exc

                return BogonIter()

            def __getitem__(self, key):
                return key

        self.assertRaises(Exc, d.update, FailingUserDict())

        class FailingUserDict:
            __module__ = __name__

            def keys(self):

                class BogonIter:
                    __module__ = __name__

                    def __init__(self):
                        self.i = ord('a')

                    def __iter__(self):
                        return self

                    def next(self):
                        if self.i <= ord('z'):
                            rtn = chr(self.i)
                            self.i += 1
                            return rtn
                        raise StopIteration

                return BogonIter()

            def __getitem__(self, key):
                raise Exc

        self.assertRaises(Exc, d.update, FailingUserDict())

        class badseq(object):
            __module__ = __name__

            def __iter__(self):
                return self

            def next(self):
                raise Exc()

        self.assertRaises(Exc, StableDict().update, badseq())
        self.assertRaises(ValueError, StableDict().update, [(1, 2, 3)])
        return

    def test_fromkeys(self):
        needsCPython(2, 3)
        self.assertEqual(StableDict.fromkeys('abc'), {'a': None, 'b': None, 'c': None})
        d = StableDict()
        self.assert_(d.fromkeys('abc') is not d)
        self.assertEqual(d.fromkeys('abc'), {'a': None, 'b': None, 'c': None})
        self.assertEqual(d.fromkeys((4, 5), 0), {4: 0, 5: 0})
        self.assertEqual(d.fromkeys([]), StableDict())

        def g():
            yield 1

        self.assertEqual(d.fromkeys(g()), {1: None})
        self.assertRaises(TypeError, StableDict().fromkeys, 3)

        class dictlike(StableDict):
            __module__ = __name__

        self.assertEqual(dictlike.fromkeys('a'), {'a': None})
        self.assertEqual(dictlike().fromkeys('a'), {'a': None})
        self.assert_(type(dictlike.fromkeys('a')) is dictlike)
        self.assert_(type(dictlike().fromkeys('a')) is dictlike)

        class mydict(StableDict):
            __module__ = __name__

            def __new__(cls):
                return UserDict.UserDict()

        ud = mydict.fromkeys('ab')
        self.assertEqual(ud, {'a': None, 'b': None})
        self.assert_(isinstance(ud, UserDict.UserDict))
        self.assertRaises(TypeError, StableDict.fromkeys)

        class Exc(Exception):
            __module__ = __name__

        class baddict1(StableDict):
            __module__ = __name__

            def __init__(self):
                raise Exc()

        self.assertRaises(Exc, baddict1.fromkeys, [1])

        class BadSeq(object):
            __module__ = __name__

            def __iter__(self):
                return self

            def next(self):
                raise Exc()

        self.assertRaises(Exc, StableDict.fromkeys, BadSeq())

        class baddict2(StableDict):
            __module__ = __name__

            def __setitem__(self, key, value):
                raise Exc()

        self.assertRaises(Exc, baddict2.fromkeys, [1])
        return

    def test_copy(self):
        d = {1: 1, 2: 2, 3: 3}
        self.assertEqual(d.copy(), {1: 1, 2: 2, 3: 3})
        self.assertEqual(StableDict().copy(), StableDict())
        self.assertRaises(TypeError, d.copy, None)
        return

    def test_get(self):
        d = StableDict()
        self.assert_(d.get('c') is None)
        self.assertEqual(d.get('c', 3), 3)
        d = {'a': 1, 'b': 2}
        self.assert_(d.get('c') is None)
        self.assertEqual(d.get('c', 3), 3)
        self.assertEqual(d.get('a'), 1)
        self.assertEqual(d.get('a', 3), 1)
        self.assertRaises(TypeError, d.get)
        self.assertRaises(TypeError, d.get, None, None, None)
        return

    def test_setdefault(self):
        d = StableDict()
        self.assert_(d.setdefault('key0') is None)
        d.setdefault('key0', [])
        self.assert_(d.setdefault('key0') is None)
        d.setdefault('key', []).append(3)
        self.assertEqual(d['key'][0], 3)
        d.setdefault('key', []).append(4)
        self.assertEqual(len(d['key']), 2)
        self.assertRaises(TypeError, d.setdefault)

        class Exc(Exception):
            __module__ = __name__

        class BadHash(object):
            __module__ = __name__
            fail = False

            def __hash__(self):
                if self.fail:
                    raise Exc()
                else:
                    return 42

        x = BadHash()
        d[x] = 42
        x.fail = True
        self.assertRaises(Exc, d.setdefault, x, [])
        return

    def test_popitem(self):
        for copymode in (-1, 1):
            for log2size in range(10):
                size = 2 ** log2size
                a = StableDict()
                b = StableDict()
                for i in range(size):
                    a[repr(i)] = i
                    if copymode < 0:
                        b[repr(i)] = i

                if copymode > 0:
                    b = a.copy()
                for i in range(size):
                    (ka, va) = ta = a.popitem()
                    self.assertEqual(va, int(ka))
                    (kb, vb) = tb = b.popitem()
                    self.assertEqual(vb, int(kb))
                    self.assert_(not (copymode < 0 and ta != tb))

                self.assert_(not a)
                self.assert_(not b)

        d = StableDict()
        self.assertRaises(KeyError, d.popitem)

    def test_pop(self):
        needsCPython(2, 3)
        d = StableDict()
        (k, v) = ('abc', 'def')
        d[k] = v
        self.assertRaises(KeyError, d.pop, 'ghi')
        self.assertEqual(d.pop(k), v)
        self.assertEqual(len(d), 0)
        self.assertRaises(KeyError, d.pop, k)
        x = 4503599627370496
        y = 4503599627370496
        h = {x: 'anything', y: 'something else'}
        self.assertEqual(h[x], h[y])
        self.assertEqual(d.pop(k, v), v)
        d[k] = v
        self.assertEqual(d.pop(k, 1), v)
        self.assertRaises(TypeError, d.pop)

        class Exc(Exception):
            __module__ = __name__

        class BadHash(object):
            __module__ = __name__
            fail = False

            def __hash__(self):
                if self.fail:
                    raise Exc()
                else:
                    return 42

        x = BadHash()
        d[x] = 42
        x.fail = True
        self.assertRaises(Exc, d.pop, x)

    def test_mutatingiteration(self):
        d = StableDict()
        d[1] = 1
        try:
            for i in d:
                d[i + 1] = 1
                assert len(d) < 10, _EmayLoopForever

        except RuntimeError:
            pass
        else:
            self.fail(_EsizeChanged)

    def test_repr(self):
        d = StableDict()
        self.assertEqual(repr(d), 'StableDict([])')
        d[1] = 2
        self.assertEqual(repr(d), 'StableDict([(1, 2)])')
        d = StableDict()
        d[1] = d
        self.assertEqual(repr(d), 'StableDict([(1, StableDict({...}))])')

        class Exc(Exception):
            __module__ = __name__

        class BadRepr(object):
            __module__ = __name__

            def __repr__(self):
                raise Exc()

        d = {1: BadRepr()}
        self.assertRaises(Exc, repr, d)

    def test_str(self):
        d = StableDict()
        self.assertEqual(str(d), 'StableDict({})')
        d[1] = 2
        self.assertEqual(str(d), 'StableDict({1: 2})')
        d = StableDict()
        d[1] = d
        self.assertEqual(str(d), 'StableDict({1: StableDict({...})})')

        class Exc(Exception):
            __module__ = __name__

        class BadRepr(object):
            __module__ = __name__

            def __repr__(self):
                raise Exc()

        d = {1: BadRepr()}
        self.assertRaises(Exc, str, d)

    def test_le(self):
        self.assert_(not StableDict() < StableDict())
        self.assert_(not {1: 2} < {1: 2})

        class Exc(Exception):
            __module__ = __name__

        class BadCmp(object):
            __module__ = __name__

            def __eq__(self, other):
                raise Exc()

        d1 = {BadCmp(): 1}
        d2 = {1: 1}
        try:
            d1 < d2
        except Exc:
            pass
        else:
            self.fail("< didn't raise Exc")

    def test_missing(self):
        needsCPython(2, 5)
        self.assertEqual(hasattr(StableDict, '__missing__'), False)
        self.assertEqual(hasattr(StableDict(), '__missing__'), False)

        class D(StableDict):
            __module__ = __name__

            def __missing__(self, key):
                return 42

        d = D({1: 2, 3: 4})
        self.assertEqual(d[1], 2)
        self.assertEqual(d[3], 4)
        self.assert_(2 not in d)
        self.assert_(2 not in d.keys())
        self.assertEqual(d[2], 42)

        class E(StableDict):
            __module__ = __name__

            def __missing__(self, key):
                raise RuntimeError(key)

        e = E()
        try:
            e[42]
        except RuntimeError, err:
            self.assertEqual(err.args, (42, ))
        else:
            self.fail("e[42] didn't raise RuntimeError")

        class F(StableDict):
            __module__ = __name__

            def __init__(self):
                self.__missing__ = lambda key: None

        f = F()
        try:
            f[42]
        except KeyError, err:
            self.assertEqual(err.args, (42, ))
        else:
            self.fail("f[42] didn't raise KeyError")

        class G(StableDict):
            __module__ = __name__

        g = G()
        try:
            g[42]
        except KeyError, err:
            self.assertEqual(err.args, (42, ))
        else:
            self.fail("g[42] didn't raise KeyError")

    def test_tuple_keyerror(self):
        needsCPython(2, 5, 1)
        d = StableDict()
        try:
            d[(1, )]
        except KeyError, e:
            self.assertEqual(e.args, ((1,), ))
        else:
            self.fail('missing KeyError')


class StableDictTest(unittest.TestCase):
    """Test key sequence stability"""
    __module__ = __name__

    def test_stability(self):
        for log2size in range(9):
            size = 2 ** log2size
            d = StableDict()
            keys = range(size)
            random.shuffle(keys)
            for k in keys:
                d[k] = -k

            self.assertEqual(keys, d.keys())
            self.assertEqual(keys, [ k for k in d ])
            self.assertEqual(keys, [ k for k in d.iterkeys() ])
            self.assertEqual(keys, [ -k for k in d.values() ])
            self.assertEqual(keys, [ -k for k in d.itervalues() ])
            items = [ (k, -k) for k in keys ]
            self.assertEqual(items, d.items())
            self.assertEqual(items, [ i for i in d.iteritems() ])
            d2 = d.copy()
            self.assertEqual(keys, d2.keys())
            d.clear()
            self.assertEqual(keys, d2.keys())
            self.assertEqual([], d.keys())
            d.update(d2)
            self.assertEqual(keys, d.keys())
            morekeys = range(size, 2 * size)
            random.shuffle(morekeys)
            for k in morekeys:
                d2[k] = -k

            d.update(d2)
            self.assertEqual(keys + morekeys, d.keys())

    def test_mutating_while_itervalues(self):
        d = StableDict()
        d[1] = 1
        try:
            for i in d.itervalues():
                d[i + 1] = i + 1
                assert len(d) < 10, _EmayLoopForever

        except RuntimeError:
            pass
        else:
            self.fail(_EsizeChanged)

    def test_mutating_while_iteritems(self):
        d = StableDict()
        d[1] = 1
        try:
            for i in d.iteritems():
                d[i[0] + 1] = i[0] + 1
                assert len(d) < 10, _EmayLoopForever

        except RuntimeError:
            pass
        else:
            self.fail(_EsizeChanged)


testClasses = [
 DictTest, StableDictTest]
try:
    from test import mapping_tests

    class GeneralMappingTests(mapping_tests.BasicTestMappingProtocol):
        __module__ = __name__
        type2test = StableDict


    class Dict(StableDict):
        __module__ = __name__


    class SubclassMappingTests(mapping_tests.BasicTestMappingProtocol):
        __module__ = __name__
        type2test = Dict


    testClasses += (GeneralMappingTests, SubclassMappingTests)
except:
    pass

def getTestSuite():
    """Return this module's test-suite."""
    warnings.filterwarnings('ignore', _WRNnoOrderArg)
    warnings.filterwarnings('ignore', _WRNnoOrderKW)
    return unittest.TestSuite(map(unittest.makeSuite, testClasses))


def test_main():
    """Run this module's test-suite."""
    test_support.run_suite(getTestSuite())


if __name__ == '__main__':
    test_main()