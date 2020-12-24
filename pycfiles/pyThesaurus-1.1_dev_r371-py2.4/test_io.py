# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyThesaurus/tests/test_io.py
# Compiled at: 2008-10-06 10:31:21
import unittest, pyThesaurus.ioSKOSCore as SKOSCore, pyThesaurus.ioDing as Ding
from pyThesaurus.Thesaurus import Thesaurus
from pyThesaurus.Concept import Concept

class testIO(unittest.TestCase):
    __module__ = __name__

    def warning(self, err):
        import sys
        sys.stderr.write('\nWarning: %s. ' % err)

    def error(self, err):
        import sys
        sys.stderr.write('\nERROR: %s\n' % err)

    def assertEqualSets(self, a, b):
        a.sort()
        b.sort()
        self.assertEqual(a, b)

    def setUp(self):
        pass

    def testSkos(self):
        t = Thesaurus()
        io = SKOSCore.ioSKOSCore('en', thesaurus=t, contexts=[])
        file = open('pyThesaurus/tests/data/sample000.rdf')
        io.read(file)
        file = open('pyThesaurus/tests/data/sample001.rdf')
        io.read(file)
        self.assertEqual(t.get_prefered('animals@en', ['en']), ['animals@en'])
        self.assertEqual(t.get_prefered('creatures@en', ['en']), ['animals@en'])
        self.assertEqual(t.get_prefered('fauna@en', ['en']), ['animals@en'])
        self.assertEqual(t.get_prefered('fauna@en', ['fr']), [])
        self.assertEqual(t.get_prefered('wetness@en', ['en']), ['wetness@en'])
        self.assertEqual(t.get_prefered('dryness@en', ['en']), ['wetness@en'])
        self.assertEqual(t.get_prefered('shrubs@en', ['en']), ['shrubs@en'])
        self.assertEqual(t.get_prefered('bushes@en', ['en']), ['shrubs@en'])
        self.assertEqual(t.get_prefered('granite@en', ['en']), ['rocks@en'])
        self.assertEqual(t('rocks@en'), t('basalt@en'))
        self.assertEqual(t('granite@en'), t('slate@en'))
        self.assertEqual(t('basalt@en'), t('slate@en'))

    def testDing(self):
        t = Thesaurus()
        io = Ding.ioDing('en', thesaurus=t, contexts=[])
        file = open('pyThesaurus/tests/data/sample000.txt')
        io.read(file)
        file = open('pyThesaurus/tests/data/sample001.txt')
        io.read(file)
        self.assertEqual(t.get_prefered('animals@en', ['en']), ['animals@en'])
        self.assertEqual(t.get_prefered('creatures@en', ['en']), ['animals@en'])
        self.assertEqual(t.get_prefered('fauna@en', ['en']), ['animals@en'])
        self.assertEqual(t.get_prefered('fauna@en', ['fr']), [])
        self.assertEqual(t.get_prefered('wetness@en', ['en']), ['wetness@en'])
        self.assertEqual(t.get_prefered('dryness@en', ['en']), ['wetness@en'])
        self.assertEqual(t.get_prefered('shrubs@en', ['en']), ['shrubs@en'])
        self.assertEqual(t.get_prefered('bushes@en', ['en']), ['shrubs@en'])
        self.assertEqual(t.get_prefered('granite@en', ['en']), ['rocks@en'])
        self.assertEqual(t('rocks@en'), t('basalt@en'))
        self.assertEqual(t('granite@en'), t('slate@en'))
        self.assertEqual(t('basalt@en'), t('slate@en'))

    def testDing2(self):
        t = Thesaurus()
        io = Ding.ioDing('es', thesaurus=t, contexts=[])
        file = open('pyThesaurus/tests/data/open_thesaurus_es.txt')
        io.read(file, encoding='latin1')
        self.assertEqual(t.get_prefered('rector@es', ['es']), ['abad@es', unicode(b'de\xe1n@es', 'latin1')])

    def testDing3(self):
        t = Thesaurus()
        c = Concept(et=['shrubs@en', 'bushes@en', 'arbuste@fr', 'buisson@fr'])
        t.append_concept(c)
        io = Ding.ioDing('en', thesaurus=t, contexts=[])
        file = open('test.txt', 'w')
        io.write(file, encoding='latin1')
        file.close()
        file = open('test.txt')
        self.assertEqual(file.readlines()[0][0:-2], 'shrubs;bushes')
        file.close()

    def testDing4(self):
        t = Thesaurus()
        io = Ding.ioDing('es', thesaurus=t, contexts=[])
        file = open('pyThesaurus/tests/data/sample002.txt')
        io.read(file)
        self.assertEqual(t.terms(), ['bushes@es', 'rocks@es', 'basalt@es', 'wetness@es', 'shrubs@es', 'dryness @es', 'granite@es', 'slate@es'])


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(testIO))
    return suite


if __name__ == '__main__':
    unittest.main()