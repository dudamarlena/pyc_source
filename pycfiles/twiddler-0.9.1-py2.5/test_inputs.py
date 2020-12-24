# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/twiddler/tests/test_inputs.py
# Compiled at: 2008-07-24 14:48:01
import os, shutil, unittest
from tempfile import mkstemp, mkdtemp
from zope.testing.doctest import DocFileSuite, REPORT_NDIFF, ELLIPSIS
from twiddler.executor.source import Source
from twiddler.output.default import Default as render

class TestDefaultParser(unittest.TestCase):

    def _makeOne(self, source='<x id="x">a<y id="y">b</y>c</x>'):
        from twiddler.input.default import Default
        return Default(source, ('id', ))

    executor = None

    def _create(self, source):
        (tree, executor) = self._makeOne(source)
        self.failUnless(executor is self.executor)
        return tree

    def test_dom(self):
        from twiddler.elementtreeplus import ElementPlus, ElementTreePlus
        (tree, executor) = self._makeOne()
        self.failUnless(isinstance(tree, ElementTreePlus))
        r = tree.getroot()
        self.failUnless(isinstance(r, ElementPlus))
        self.assertEqual(len(r), 1)
        self.assertEqual(r.tag, False)
        self.assertEqual(r.text, None)
        self.assertEqual(r.tail, None)
        self.assertEqual(r.items(), [])
        x = r[0]
        self.failUnless(isinstance(x, ElementPlus))
        self.assertEqual(len(x), 2)
        self.assertEqual(x.tag, 'x')
        self.assertEqual(x.text, 'a')
        self.assertEqual(x.tail, None)
        self.assertEqual(x.items(), [('id', 'x')])
        y = x[0]
        self.failUnless(isinstance(y, ElementPlus))
        self.assertEqual(len(y), 0)
        self.assertEqual(y.tag, 'y')
        self.assertEqual(y.text, 'b')
        self.assertEqual(y.tail, '')
        self.assertEqual(y.items(), [('id', 'y')])
        ay = x[1]
        self.failUnless(isinstance(ay, ElementPlus))
        self.assertEqual(len(ay), 0)
        self.assertEqual(ay.tag, False)
        self.assertEqual(ay.text, 'c')
        self.assertEqual(ay.tail, None)
        self.assertEqual(ay.items(), [])
        self.failUnless(tree.findByAttribute('id', 'x') is x)
        self.failUnless(tree.findByAttribute('id', 'y') is y)
        return

    def test_tail_1(self):
        from twiddler.elementtreeplus import ElementPlus, ElementTreePlus
        tree = self._create('<top><x/> \n</top>')
        self.failUnless(isinstance(tree, ElementTreePlus))
        r = tree.getroot()
        self.failUnless(isinstance(r, ElementPlus))
        self.assertEqual(len(r), 1)
        self.assertEqual(r.tag, False)
        self.assertEqual(r.text, None)
        self.assertEqual(r.tail, None)
        self.assertEqual(r.items(), [])
        top = r[0]
        self.failUnless(isinstance(top, ElementPlus))
        self.assertEqual(len(top), 1)
        self.assertEqual(top.tag, 'top')
        self.assertEqual(top.text, None)
        self.assertEqual(top.tail, None)
        self.assertEqual(top.items(), [])
        x = top[0]
        self.failUnless(isinstance(x, ElementPlus))
        self.assertEqual(len(x), 0)
        self.assertEqual(x.tag, 'x')
        self.assertEqual(x.text, None)
        self.assertEqual(x.tail, ' \n')
        self.assertEqual(x.items(), [])
        return

    def test_tail_2(self):
        from twiddler.elementtreeplus import ElementPlus, ElementTreePlus
        tree = self._create('<top><x/>y \nz</top>')
        self.failUnless(isinstance(tree, ElementTreePlus))
        r = tree.getroot()
        self.failUnless(isinstance(r, ElementPlus))
        self.assertEqual(len(r), 1)
        self.assertEqual(r.tag, False)
        self.assertEqual(r.text, None)
        self.assertEqual(r.tail, None)
        self.assertEqual(r.items(), [])
        top = r[0]
        self.failUnless(isinstance(top, ElementPlus))
        self.assertEqual(len(top), 2)
        self.assertEqual(top.tag, 'top')
        self.assertEqual(top.text, None)
        self.assertEqual(top.tail, None)
        self.assertEqual(top.items(), [])
        x = top[0]
        self.failUnless(isinstance(x, ElementPlus))
        self.assertEqual(len(x), 0)
        self.assertEqual(x.tag, 'x')
        self.assertEqual(x.text, None)
        self.assertEqual(x.tail, '')
        self.assertEqual(x.items(), [])
        tail = top[1]
        self.failUnless(isinstance(tail, ElementPlus))
        self.assertEqual(len(tail), 0)
        self.assertEqual(tail.tag, False)
        self.assertEqual(tail.text, 'y \nz')
        self.assertEqual(tail.tail, None)
        self.assertEqual(tail.items(), [])
        return


class TestDefaultParserWithCodeBlockNoCode(TestDefaultParser):
    executor = False

    def _makeOne(self, source='<x id="x">a<y id="y">b</y>c</x>'):
        from twiddler.input.default import DefaultWithCodeBlock
        return DefaultWithCodeBlock(source, ('id', ))


class TestDefaultParserWithCodeBlock(TestDefaultParser):
    executor = False

    def _makeOne(self, source='<!--twiddler def x(t): pass--><x id="x">a<y id="y">b</y>c</x>'):
        from twiddler.input.default import DefaultWithCodeBlock
        return DefaultWithCodeBlock(source, ('id', ))

    def test_code(self):
        (tree, executor) = self._makeOne()
        self.failUnless(isinstance(executor, Source))
        self.assertEqual(executor.source, 'def x(t): pass\n')

    def test_no_code(self):
        (tree, executor) = self._makeOne(source='<x id="x">a<y id="y">b</y>c</x>')
        self.failUnless(executor is False)

    def test_no_source(self):
        (tree, executor) = self._makeOne(source='')
        self.failUnless(executor is False)


class TestPlainText(unittest.TestCase):

    def _create(self, source):
        from twiddler.input.plaintext import PlainText
        (tree, executor) = PlainText(source, ('id', ))
        self.assertEqual(executor, None)
        return tree

    def test_nothing(self):
        from twiddler.elementtreeplus import ElementPlus, ElementTreePlus
        tree = self._create('')
        self.failUnless(isinstance(tree, ElementTreePlus))
        r = tree.getroot()
        self.failUnless(isinstance(r, ElementPlus))
        self.assertEqual(len(r), 0)
        self.assertEqual(r.tag, False)
        self.assertEqual(r.text, '')
        self.assertEqual(r.tail, None)
        self.assertEqual(r.items(), [])
        result = render(tree)
        self.failUnless(isinstance(result, unicode))
        self.assertEqual(result, '')
        return

    def test_just_text(self):
        from twiddler.elementtreeplus import ElementPlus, ElementTreePlus
        tree = self._create('1234')
        self.failUnless(isinstance(tree, ElementTreePlus))
        r = tree.getroot()
        self.failUnless(isinstance(r, ElementPlus))
        self.assertEqual(len(r), 0)
        self.assertEqual(r.tag, False)
        self.assertEqual(r.text, '1234')
        self.assertEqual(r.tail, None)
        self.assertEqual(r.items(), [])
        result = render(tree)
        self.failUnless(isinstance(result, unicode))
        self.assertEqual(result, '1234')
        return

    def test_single_sub(self):
        from twiddler.elementtreeplus import ElementPlus, ElementTreePlus
        tree = self._create('$a')
        self.failUnless(isinstance(tree, ElementTreePlus))
        r = tree.getroot()
        self.failUnless(isinstance(r, ElementPlus))
        self.assertEqual(len(r), 1)
        self.assertEqual(r.tag, False)
        self.assertEqual(r.text, '')
        self.assertEqual(r.tail, None)
        self.assertEqual(r.items(), [])
        a = r[0]
        self.failUnless(isinstance(a, ElementPlus))
        self.assertEqual(len(a), 0)
        self.assertEqual(a.tag, False)
        self.assertEqual(a.text, '$a')
        self.assertEqual(a.tail, None)
        self.assertEqual(a.items(), [('id', 'a')])
        result = render(tree)
        self.failUnless(isinstance(result, unicode))
        self.assertEqual(result, '$a')
        self.failUnless(tree.search('a') is a)
        return

    def test_single_sec(self):
        from twiddler.elementtreeplus import ElementPlus, ElementTreePlus
        tree = self._create('<a>\n</a>')
        self.failUnless(isinstance(tree, ElementTreePlus))
        r = tree.getroot()
        self.failUnless(isinstance(r, ElementPlus))
        self.assertEqual(len(r), 1)
        self.assertEqual(r.tag, False)
        self.assertEqual(r.text, '')
        self.assertEqual(r.tail, None)
        self.assertEqual(r.items(), [])
        a = r[0]
        self.failUnless(isinstance(a, ElementPlus))
        self.assertEqual(len(a), 0)
        self.assertEqual(a.tag, False)
        self.assertEqual(a.text, '\n')
        self.assertEqual(a.tail, '')
        self.assertEqual(a.items(), [('id', 'a')])
        result = render(tree)
        self.failUnless(isinstance(result, unicode))
        self.assertEqual(result, '\n')
        self.failUnless(tree.search('a') is a)
        return

    def test_sub_only(self):
        from twiddler.elementtreeplus import ElementPlus, ElementTreePlus
        tree = self._create('1$a 2$b 3')
        self.failUnless(isinstance(tree, ElementTreePlus))
        r = tree.getroot()
        self.failUnless(isinstance(r, ElementPlus))
        self.assertEqual(len(r), 4)
        self.assertEqual(r.tag, False)
        self.assertEqual(r.text, '1')
        self.assertEqual(r.tail, None)
        self.assertEqual(r.items(), [])
        a = r[0]
        self.failUnless(isinstance(a, ElementPlus))
        self.assertEqual(len(a), 0)
        self.assertEqual(a.tag, False)
        self.assertEqual(a.text, '$a')
        self.assertEqual(a.tail, None)
        self.assertEqual(a.items(), [('id', 'a')])
        aa = r[1]
        self.failUnless(isinstance(aa, ElementPlus))
        self.assertEqual(len(aa), 0)
        self.assertEqual(aa.tag, False)
        self.assertEqual(aa.text, ' 2')
        self.assertEqual(aa.tail, None)
        self.assertEqual(aa.items(), [])
        b = r[2]
        self.failUnless(isinstance(b, ElementPlus))
        self.assertEqual(len(b), 0)
        self.assertEqual(b.tag, False)
        self.assertEqual(b.text, '$b')
        self.assertEqual(b.tail, None)
        self.assertEqual(b.items(), [('id', 'b')])
        ab = r[3]
        self.failUnless(isinstance(ab, ElementPlus))
        self.assertEqual(len(ab), 0)
        self.assertEqual(ab.tag, False)
        self.assertEqual(ab.text, ' 3')
        self.assertEqual(ab.tail, None)
        self.assertEqual(ab.items(), [])
        result = render(tree)
        self.failUnless(isinstance(result, unicode))
        self.assertEqual(result, '1$a 2$b 3')
        self.failUnless(tree.search('a') is a)
        self.failUnless(tree.search('b') is b)
        return

    def test_sec_only(self):
        from twiddler.elementtreeplus import ElementPlus, ElementTreePlus
        tree = self._create('1<a>2<b>3</b>4</a> 5<c>6</c>7 8')
        self.failUnless(isinstance(tree, ElementTreePlus))
        r = tree.getroot()
        self.failUnless(isinstance(r, ElementPlus))
        self.assertEqual(len(r), 4)
        self.assertEqual(r.tag, False)
        self.assertEqual(r.text, '1')
        self.assertEqual(r.tail, None)
        self.assertEqual(r.items(), [])
        a = r[0]
        self.failUnless(isinstance(a, ElementPlus))
        self.assertEqual(len(a), 2)
        self.assertEqual(a.tag, False)
        self.assertEqual(a.text, '2')
        self.assertEqual(a.tail, ' ')
        self.assertEqual(a.items(), [('id', 'a')])
        b = a[0]
        self.failUnless(isinstance(b, ElementPlus))
        self.assertEqual(len(b), 0)
        self.assertEqual(b.tag, False)
        self.assertEqual(b.text, '3')
        self.assertEqual(b.tail, '')
        self.assertEqual(b.items(), [('id', 'b')])
        ab = a[1]
        self.failUnless(isinstance(ab, ElementPlus))
        self.assertEqual(len(ab), 0)
        self.assertEqual(ab.tag, False)
        self.assertEqual(ab.text, '4')
        self.assertEqual(ab.tail, None)
        self.assertEqual(ab.items(), [])
        aa = r[1]
        self.failUnless(isinstance(aa, ElementPlus))
        self.assertEqual(len(aa), 0)
        self.assertEqual(aa.tag, False)
        self.assertEqual(aa.text, '5')
        self.assertEqual(aa.tail, None)
        self.assertEqual(aa.items(), [])
        c = r[2]
        self.failUnless(isinstance(c, ElementPlus))
        self.assertEqual(len(c), 0)
        self.assertEqual(c.tag, False)
        self.assertEqual(c.text, '6')
        self.assertEqual(c.tail, '')
        self.assertEqual(c.items(), [('id', 'c')])
        ac = r[3]
        self.failUnless(isinstance(ac, ElementPlus))
        self.assertEqual(len(ac), 0)
        self.assertEqual(ac.tag, False)
        self.assertEqual(ac.text, '7 8')
        self.assertEqual(ac.tail, None)
        self.assertEqual(ac.items(), [])
        result = render(tree)
        self.failUnless(isinstance(result, unicode))
        self.assertEqual(result, '1234 567 8')
        self.failUnless(tree.search('a') is a)
        self.failUnless(tree.search('b') is b)
        self.failUnless(tree.search('c') is c)
        return

    def test_mixed(self):
        from twiddler.elementtreeplus import ElementPlus, ElementTreePlus
        tree = self._create('1<a>2<b>3$c 4</b>  </a>6<d>7</d>8$e 9')
        self.failUnless(isinstance(tree, ElementTreePlus))
        r = tree.getroot()
        self.failUnless(isinstance(r, ElementPlus))
        self.assertEqual(len(r), 6)
        self.assertEqual(r.tag, False)
        self.assertEqual(r.text, '1')
        self.assertEqual(r.tail, None)
        self.assertEqual(r.items(), [])
        a = r[0]
        self.failUnless(isinstance(a, ElementPlus))
        self.assertEqual(len(a), 1)
        self.assertEqual(a.tag, False)
        self.assertEqual(a.text, '2')
        self.assertEqual(a.tail, '')
        self.assertEqual(a.items(), [('id', 'a')])
        b = a[0]
        self.failUnless(isinstance(b, ElementPlus))
        self.assertEqual(len(b), 2)
        self.assertEqual(b.tag, False)
        self.assertEqual(b.text, '3')
        self.assertEqual(b.tail, '  ')
        self.assertEqual(b.items(), [('id', 'b')])
        c = b[0]
        self.failUnless(isinstance(c, ElementPlus))
        self.assertEqual(len(c), 0)
        self.assertEqual(c.tag, False)
        self.assertEqual(c.text, '$c')
        self.assertEqual(c.tail, None)
        self.assertEqual(c.items(), [('id', 'c')])
        ac = b[1]
        self.failUnless(isinstance(ac, ElementPlus))
        self.assertEqual(len(ac), 0)
        self.assertEqual(ac.tag, False)
        self.assertEqual(ac.text, ' 4')
        self.assertEqual(ac.tail, None)
        self.assertEqual(ac.items(), [])
        aa = r[1]
        self.failUnless(isinstance(aa, ElementPlus))
        self.assertEqual(len(aa), 0)
        self.assertEqual(aa.tag, False)
        self.assertEqual(aa.text, '6')
        self.assertEqual(aa.tail, None)
        self.assertEqual(aa.items(), [])
        d = r[2]
        self.failUnless(isinstance(d, ElementPlus))
        self.assertEqual(len(d), 0)
        self.assertEqual(d.tag, False)
        self.assertEqual(d.text, '7')
        self.assertEqual(d.tail, '')
        self.assertEqual(d.items(), [('id', 'd')])
        ad = r[3]
        self.failUnless(isinstance(ad, ElementPlus))
        self.assertEqual(len(ad), 0)
        self.assertEqual(ad.tag, False)
        self.assertEqual(ad.text, '8')
        self.assertEqual(ad.tail, None)
        self.assertEqual(ad.items(), [])
        e = r[4]
        self.failUnless(isinstance(e, ElementPlus))
        self.assertEqual(len(e), 0)
        self.assertEqual(e.tag, False)
        self.assertEqual(e.text, '$e')
        self.assertEqual(e.tail, None)
        self.assertEqual(e.items(), [('id', 'e')])
        ae = r[5]
        self.failUnless(isinstance(ae, ElementPlus))
        self.assertEqual(len(ae), 0)
        self.assertEqual(ae.tag, False)
        self.assertEqual(ae.text, ' 9')
        self.assertEqual(ae.tail, None)
        self.assertEqual(ae.items(), [])
        result = render(tree)
        self.failUnless(isinstance(result, unicode))
        self.assertEqual(result, '123$c 4  678$e 9')
        self.failUnless(tree.search('a') is a)
        self.failUnless(tree.search('b') is b)
        self.failUnless(tree.search('c') is c)
        self.failUnless(tree.search('d') is d)
        self.failUnless(tree.search('e') is e)
        return


def FileWrapperSetUp(test):
    (fp, test.twiddler_path) = mkstemp()
    os.close(fp)
    test.globs['test_path'] = test.twiddler_path
    test.twiddler_dir = mkdtemp()
    test.globs['test_dir'] = test.twiddler_dir


def FileWrapperTearDown(test):
    os.remove(test.twiddler_path)
    shutil.rmtree(test.twiddler_dir)


options = REPORT_NDIFF | ELLIPSIS

def test_suite():
    return unittest.TestSuite((
     DocFileSuite('../input/default.txt', optionflags=options),
     DocFileSuite('../input/plaintext.txt', optionflags=options),
     DocFileSuite('../input/filewrapper.txt', optionflags=options, setUp=FileWrapperSetUp, tearDown=FileWrapperTearDown),
     unittest.makeSuite(TestDefaultParser),
     unittest.makeSuite(TestDefaultParserWithCodeBlockNoCode),
     unittest.makeSuite(TestDefaultParserWithCodeBlock),
     unittest.makeSuite(TestPlainText)))


if __name__ == '__main__':
    unittest.main(default='test_suite')