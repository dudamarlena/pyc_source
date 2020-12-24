# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyThesaurus/tests/test_persistence.py
# Compiled at: 2008-10-06 10:31:21
process = True
try:
    import ZODB, ZODB.FileStorage
except:
    try:
        import sys
        sys.path.append('../../parts/zope2/lib/python/')
        import ZODB, ZODB.FileStorage, transaction, persistent
    except:
        process = False

import unittest
from pyThesaurus.Thesaurus import Thesaurus
from pyThesaurus.Concept import Concept
import pyThesaurus.ioSKOSCore as SKOSCore

class testPersistence(unittest.TestCase):
    __module__ = __name__
    _count = 10

    def warning(self, err):
        import sys
        sys.stderr.write('\nWarning: %s. ' % err)

    def error(self, err):
        import sys
        sys.stderr.write('\nERROR: %s. ' % err)

    def assertEqualSets(self, a, b):
        a.sort()
        b.sort()
        self.assertEqual(a, b)

    def createDB(self):
        if not process:
            return
        db = ZODB.DB(ZODB.FileStorage.FileStorage('test.fs', create=1))
        self._db = db
        self._root = db.open().root()
        self._root['loadThesauri'] = False
        transaction.commit()

    def openDB(self):
        if not process:
            return
        db = ZODB.DB(ZODB.FileStorage.FileStorage('test.fs', create=0))
        self._db = db
        self._root = db.open().root()

    def closeDB(self):
        if not process:
            return
        self._db.close()
        self._db = None
        self._root = None
        return

    def loadThesauri(self):
        if not process:
            return
        if self._root['loadThesauri']:
            return
        for i in range(self._count):
            skosfile = open('pyThesaurus/tests/data/sample%03i.rdf' % i)
            t = SKOSCore.load(skosfile, 'en')
            self._root['sample%03i' % i] = t

        self._root['loadThesauri'] = True
        transaction.commit()

    def delThesauri(self):
        if not process:
            return
        if not self._root['loadThesauri']:
            return
        for i in range(self._count):
            del self._root['sample%03i' % i]

        if 'ukat' in self._root['ukat']:
            del slef._root['ukat']
        self._root['loadThesauri'] = False
        transaction.commit()

    def testCreateThesaurus(self):
        if not process:
            return
        self.createDB()
        self.delThesauri()
        self.loadThesauri()
        t = self._root['sample000']
        self.assertEqual(t.get_prefered('animals@en', ['en']), ['animals@en'])
        self.assertEqual(t.get_prefered('creatures@en', ['en']), ['animals@en'])
        self.assertEqual(t.get_prefered('fauna@en', ['en']), ['animals@en'])
        self.assertEqual(t.get_prefered('fauna@en', ['fr']), [])
        self.closeDB()

    def testOpenThesaurus(self):
        if not process:
            return
        self.createDB()
        self.delThesauri()
        self.loadThesauri()
        self.closeDB()
        self.openDB()
        self.assertEqualSets([ 'sample%03i' % i for i in range(self._count) ] + ['loadThesauri'], self._root.keys())
        t = self._root['sample000']
        self.assertEqual(t.get_prefered('animals@en', ['en']), ['animals@en'])
        self.assertEqual(t.get_prefered('creatures@en', ['en']), ['animals@en'])
        self.assertEqual(t.get_prefered('fauna@en', ['en']), ['animals@en'])
        self.assertEqual(t.get_prefered('fauna@en', ['fr']), [])
        t = self._root['sample001']
        self.assertEqual(t.get_prefered('wetness@en', ['en']), ['wetness@en'])
        self.assertEqual(t.get_prefered('dryness@en', ['en']), ['wetness@en'])
        self.assertEqual(t.get_prefered('shrubs@en', ['en']), ['shrubs@en'])
        self.assertEqual(t.get_prefered('bushes@en', ['en']), ['shrubs@en'])
        self.assertEqual(t.get_prefered('granite@en', ['en']), ['rocks@en'])
        self.assertEqual(t('rocks@en'), t('basalt@en'))
        self.assertEqual(t('granite@en'), t('slate@en'))
        self.assertEqual(t('basalt@en'), t('slate@en'))
        t = self._root['sample002']
        self.assertEqual(t('abattoirs@en'), t('abattoirs@en'))
        self.assertEqual(t('abatoirs@en'), t('abattoirs@en'))
        self.assertEqual(t('abbatoirs@en'), t('abattoirs@en'))
        self.assertEqual(t('abbattoirs@en'), t('abattoirs@en'))
        self.assertEqualSets(t.get_equivalent('abbattoirs@en', ['es', 'en']), ['abattoirs@en'])
        t = self._root['sample003']
        self.assertEqual(t('shrubs@en'), t('shrubs@en'))
        self.assertEqual(t('bushes@en'), t('shrubs@en'))
        self.assertEqual(t('arbuste@fr'), t('shrubs@en'))
        self.assertEqual(t('buisson@fr'), t('shrubs@en'))
        self.assertEqualSets(t.get_prefered('buisson@fr', ['fr', 'en']), ['shrubs@en', 'arbuste@fr'])
        self.assertEqualSets(t.get_prefered('buisson@fr', ['en']), ['shrubs@en'])
        self.assertEqualSets(t.get_prefered('buisson@fr', ['fr']), ['arbuste@fr'])
        self.closeDB()

    def testLoadBigThesauri(self):
        if not process:
            return
        self.createDB()
        self.delThesauri()
        skosfile = open('pyThesaurus/tests/data/ukat_concepts.rdf')
        t = SKOSCore.load(skosfile, 'en')
        self._root['ukat'] = t
        transaction.commit()
        self.closeDB()
        self.openDB()
        t = self._root['ukat']
        self.assertEqualSets(t.get_narrower('Educational sciences and environment@en', ['en']), ['Education and skills@en', 'Education@en', 'Educational environment@en', 'Educational sciences@en', 'Girls education@en', 'ICT education at school@en', 'Information and communication technologies education at school@en', 'Labor unions and education@en', 'Learning and scholarship@en', 'Learning environment@en', 'Learning@en', 'Libraries and education@en', 'Medieval education@en', 'Pedagogy@en', 'Socialism and education@en', 'Sound recordings in education@en', 'Studies@en', 'Study and teaching@en', 'Trade unions and education@en', 'Volunteer workers in education@en', 'Womens education@en'])
        self.assertEqualSets(t.get_broader('Educational sciences and environment@en', ['en']), [])
        self.assertEqualSets(t.get_narrower('Educational policy@en', ['en']), ['Adult literacy@en', 'Advancement of education@en', 'Alternative education@en', 'Anticurriculum movement@en', 'Business links with schools@en', 'Church and college@en', 'Church and education@en', 'Community and education@en', 'Community links with schools@en', 'Computer uses in education@en', 'Computers for learning applications@en', 'Deschooling@en', 'Education and culture@en', 'Education and state@en', 'Educational aims@en', 'Educational alternatives@en', 'Educational computing@en', 'Educational development@en', 'Educational discrimination@en', 'Educational goals@en', 'Educational objectives@en', 'Educational policy@en', 'Educational strategies@en', 'Higher education and state@en', 'Industry and education@en', 'International cooperation education@en', 'International education@en', 'International understanding education@en', 'Language of instruction@en', 'Leisure and education@en', 'Leisure education@en', 'Right to education@en', 'Role of education@en', 'School industry relationship@en', 'State and education@en', 'Study abroad@en', 'Training abroad@en', 'Transnational education@en', 'Values education@en'])
        self.assertEqualSets(t.get_broader('Educational policy@en', ['en']), [])
        self.assertEqualSets(t.get_narrower('Poems@en', ['en']), [])
        self.assertEqualSets(t.get_broader('Poems@en', ['en']), ['Basque poetry@en', 'Belgian poetry (French)@en', 'Breton poetry@en', 'Chinese poetry@en', 'English dialect poetry@en', 'English poems@en', 'English poetry@en', 'English prose poems@en', 'French poetry@en', 'German poetry@en', 'Greek poetry@en', 'Irish poetry@en', 'Italian poetry@en', 'Latin poetry@en', 'Medieval poetry@en', 'Middle English poetry@en', 'Persian poetry@en', 'Poetry@en', 'Russian poetry@en', 'Scottish poetry@en', 'Spanish poetry@en', 'Verse@en', 'Welsh poetry@en'])
        self.closeDB()

    def test_emanuel01_bug(self):
        if not process:
            return
        self.createDB()
        self.delThesauri()
        self.loadThesauri()
        self.closeDB()
        self.openDB()
        t = self._root['sample001']
        t.append_term('fútbol@es', et=['balón pie@es', 'soccer@en', 'football@en', 'football@fr'])
        self._root['sample001'] = t
        transaction.commit()
        self.closeDB()
        self.openDB()
        t = self._root['sample001']
        self.assertEqualSets(t.get_equivalent('fútbol@es', ['es', 'en', 'fr']), ['fútbol@es', 'balón pie@es', 'soccer@en', 'football@en', 'football@fr'])
        self.closeDB()


def test_suite():
    import pdb
    suite.addTest(unittest.makeSuite(testPersistence))
    return suite