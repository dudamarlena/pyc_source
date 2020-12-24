# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\pycurry\test\gof.py
# Compiled at: 2009-08-08 07:36:35
__doc__ = 'Tests for the gof module.\n\nCopyright (c) 2008 Fons Dijkstra\n\nPermission is hereby granted, free of charge, to any person obtaining a copy\nof this software and associated documentation files (the "Software"), to deal\nin the Software without restriction, including without limitation the rights\nto use, copy, modify, merge, publish, distribute, sublicense, and/or sell\ncopies of the Software, and to permit persons to whom the Software is\nfurnished to do so, subject to the following conditions:\n\nThe above copyright notice and this permission notice shall be included in\nall copies or substantial portions of the Software.\n\nTHE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\nIMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\nFITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\nAUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\nLIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\nOUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN\nTHE SOFTWARE.\n'
import pycurry.dbc as dbc
dbc.level.set(dbc.level.max())
import sys, unittest, pycurry.tst as tst, pycurry.gof as sut

class composite(unittest.TestCase):

    def setUp(self):
        self.__sut = sut.composite()

    def test_repr(self):
        repr(self.__sut)

    def test_str(self):
        str(self.__sut)

    def test_parent(self):
        self.failUnless(self.__sut.parent is None)
        return

    def test_capacity(self):
        self.failUnlessEqual(self.__sut.capacity, sys.maxint)

    def test_len(self):
        self.failUnlessEqual(len(self.__sut), 0)

    def test_in(self):
        self.failIf(self.__sut in self.__sut)

    def test_iter(self):
        for child in self.__sut:
            self.fail('sut has no children')

    def test_root(self):
        self.failUnless(self.__sut.root)

    def test_empty(self):
        self.failUnless(self.__sut.empty)

    def test_full(self):
        self.failIf(self.__sut.full)

    def test_add(self):
        self.__sut.add(sut.leaf())

    def test_remove(self):
        child = sut.composite()
        self.__sut.add(child)
        self.__sut.remove(child)


class leaf(unittest.TestCase):

    def setUp(self):
        self.__sut = sut.leaf()

    def test_repr(self):
        repr(self.__sut)

    def test_str(self):
        str(self.__sut)

    def test_parent(self):
        self.failUnless(self.__sut.parent is None)
        return

    def test_capacity(self):
        self.failUnlessEqual(self.__sut.capacity, 0)

    def test_len(self):
        self.failUnlessEqual(len(self.__sut), 0)

    def test_in(self):
        self.failIf(self.__sut in self.__sut)

    def test_iter(self):
        for child in self.__sut:
            self.fail('sut has no children')

    def test_root(self):
        self.failUnless(self.__sut.root)

    def test_empty(self):
        self.failUnless(self.__sut.empty)

    def test_full(self):
        self.failUnless(self.__sut.full)


class config(unittest.TestCase):

    def test_leaf_attrs(self):
        leaf = sut.leaf(attrs={'a': NotImplemented})
        self.failUnless(leaf.a is NotImplemented)
        leaf.a = None
        self.failUnless(leaf.a is None)
        return

    def test_comp_attrs(self):
        comp = sut.composite(attrs={'a': NotImplemented})
        self.failUnless(comp.a is NotImplemented)
        comp.a = None
        self.failUnless(comp.a is None)
        return

    def test_comp_set(self):
        comp = sut.composite(container=set)
        leaf = sut.leaf()
        comp.add(leaf)
        comp.remove(leaf)

    def test_comp_list(self):
        comp = sut.composite(container=list)
        leaf = sut.leaf()
        comp.add(leaf)
        comp.remove(leaf)


class usage(unittest.TestCase):

    def setUp(self):
        self.__root = sut.composite(attrs={'name': 'root'})
        self.__elem = sut.composite(attrs={'name': 'elem'}, container=list)
        self.__a = sut.leaf(attrs={'name': 'a'})
        self.__b = sut.leaf(attrs={'name': 'b'})
        self.__c = sut.leaf(attrs={'name': 'c'})
        self.__root.add(self.__elem)
        self.__elem.add(self.__a)
        self.__elem.add(self.__b)
        self.__root.add(self.__c)

    def _test(self):
        pass


def suite():
    return unittest.TestSuite([
     unittest.TestLoader().loadTestsFromTestCase(composite),
     unittest.TestLoader().loadTestsFromTestCase(leaf),
     unittest.TestLoader().loadTestsFromTestCase(config),
     unittest.TestLoader().loadTestsFromTestCase(usage)])


if __name__ == '__main__':
    tst.main(suite(), [sut])