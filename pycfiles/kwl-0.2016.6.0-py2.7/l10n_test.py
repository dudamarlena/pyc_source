# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-intel/egg/kwl2text/l10n_test.py
# Compiled at: 2016-01-29 11:34:28
import l10n as l, unittest

class L10nTest(unittest.TestCase):

    def setUp(self):
        pass

    def testPlurals(self):
        self.assertEquals('nkua', l.plural('akan', 'kua'))
        self.assertEquals('mbusua', l.plural('akan', 'busua'))
        self.assertEquals('lɔre', l.plural('akan', 'lɔre'))
        self.assertEquals('bɔɔl', l.plural('akan', 'bɔɔl'))
        self.assertEquals('bɔɔlbɔ', l.plural('akan', 'bɔɔlbɔ'))
        self.assertEquals('skuulkɔ', l.plural('akan', 'skuulkɔ'))
        self.assertEquals('dwumayɛ', l.plural('akan', 'dwumayɛ'))


if __name__ == '__main__':
    unittest.main()