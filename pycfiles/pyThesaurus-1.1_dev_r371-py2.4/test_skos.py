# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyThesaurus/tests/test_skos.py
# Compiled at: 2008-10-06 10:31:21
import unittest, pyThesaurus.ioSKOSCore as SKOSCore
from pyThesaurus.Thesaurus import Thesaurus
from pyThesaurus.Concept import Concept

class testSKOSCore(unittest.TestCase):
    __module__ = __name__

    def warning(self, err):
        import sys
        sys.stderr.write('\nWarning: %s.\n' % err)

    def error(self, err):
        import sys
        sys.stderr.write('\nERROR: %s\n' % err)

    def assertEqualSets(self, a, b):
        a.sort()
        b.sort()
        self.assertEqual(a, b)

    def setUp(self):
        pass

    def testLoadConcept(self):
        """
                """
        file = open('pyThesaurus/tests/data/sample000.rdf')
        t = Thesaurus()
        io = SKOSCore.ioSKOSCore('en', thesaurus=t, contexts=[])
        io.read(file)
        self.assertEqual(t.get_prefered('animals@en', ['en']), ['animals@en'])
        self.assertEqual(t.get_prefered('creatures@en', ['en']), ['animals@en'])
        self.assertEqual(t.get_prefered('fauna@en', ['en']), ['animals@en'])
        self.assertEqual(t.get_prefered('fauna@en', ['fr']), [])

    def testLoadLabellingProperties(self):
        """
                |
                |
                |
                """
        file = open('pyThesaurus/tests/data/sample001.rdf')
        t = Thesaurus()
        io = SKOSCore.ioSKOSCore('en', thesaurus=t, contexts=[])
        io.read(file)
        self.assertEqual(t.get_prefered('wetness@en', ['en']), ['wetness@en'])
        self.assertEqual(t.get_prefered('dryness@en', ['en']), ['wetness@en'])
        self.assertEqual(t.get_prefered('shrubs@en', ['en']), ['shrubs@en'])
        self.assertEqual(t.get_prefered('bushes@en', ['en']), ['shrubs@en'])
        self.assertEqual(t.get_prefered('granite@en', ['en']), ['rocks@en'])
        self.assertEqual(t('rocks@en'), t('basalt@en'))
        self.assertEqual(t('granite@en'), t('slate@en'))
        self.assertEqual(t('basalt@en'), t('slate@en'))
        file = open('pyThesaurus/tests/data/sample002.rdf')
        t = Thesaurus()
        io = SKOSCore.ioSKOSCore('en', thesaurus=t, contexts=[])
        io.read(file)
        self.assertEqual(t('abattoirs@en'), t('abattoirs@en'))
        self.assertEqual(t('abatoirs@en'), t('abattoirs@en'))
        self.assertEqual(t('abbatoirs@en'), t('abattoirs@en'))
        self.assertEqual(t('abbattoirs@en'), t('abattoirs@en'))
        self.assertEqualSets(t.get_equivalent('abbattoirs@en', ['es', 'en']), ['abattoirs@en'])
        file = open('pyThesaurus/tests/data/sample003.rdf')
        t = Thesaurus()
        io = SKOSCore.ioSKOSCore('en', thesaurus=t, contexts=[])
        io.read(file)
        self.assertEqual(t('shrubs@en'), t('shrubs@en'))
        self.assertEqual(t('bushes@en'), t('shrubs@en'))
        self.assertEqual(t('arbuste@fr'), t('shrubs@en'))
        self.assertEqual(t('buisson@fr'), t('shrubs@en'))
        self.assertEqualSets(t.get_prefered('buisson@fr', ['fr', 'en']), ['shrubs@en', 'arbuste@fr'])
        self.assertEqualSets(t.get_prefered('buisson@fr', ['en']), ['shrubs@en'])
        self.assertEqualSets(t.get_prefered('buisson@fr', ['fr']), ['arbuste@fr'])
        file = open('pyThesaurus/tests/data/sample004.rdf')
        t = Thesaurus()
        io = SKOSCore.ioSKOSCore('en', thesaurus=t, contexts=[])
        io.read(file)
        self.warning('prefSymbol, altSymbol are not implemented in this version')

    def testLoadDocumentationProperties(self):
        """
                |
                |
                |
                """
        file = open('pyThesaurus/tests/data/sample005.rdf')
        t = Thesaurus()
        io = SKOSCore.ioSKOSCore('en', thesaurus=t, contexts=[])
        io.read(file)
        self.assertEqualSets(t.get_prefered('banana republic@en', 'en'), ['banana republic@en'])
        self.assertEqualSets(t('banana republic@en'), [0])
        self.assertEqual(t.get_publicNotes(t('banana republic@en')[0])['definition'][0], 'A small country, especially in South and Central America, that is\n\t\tpoor and often badly and immorally ruled.@en')
        file = open('pyThesaurus/tests/data/sample006.rdf')
        t = Thesaurus()
        io = SKOSCore.ioSKOSCore('en', thesaurus=t, contexts=[])
        io.read(file)
        self.assertEqualSets(t.get_prefered('pineapples@en', 'fr'), ['ananas@fr'])
        self.assertEqualSets(t.get_publicNotes(t('pineapples@en')[0])['definition'], [
         unicode('The fruit of plants of the family Bromeliaceae.@en', 'latin1'), unicode(b'Le fruit de la plante herbac\xe9e de la famille des brom\xe9liac\xe9es.@fr', 'latin1')])
        file = open('pyThesaurus/tests/data/sample007.rdf')
        t = Thesaurus()
        io = SKOSCore.ioSKOSCore('en', thesaurus=t, contexts=[])
        io.read(file)
        self.assertEqualSets(t.get_publicNotes(t('notebook computers@en')[0])['changenote'], [{'value': "The preferred label for this concept changed from 'laptop computers' to 'notebook computers' on 23 Jan 1999.", 'creator': {'person': {'mbox': 'mailto:jsmith@example.org', 'name': 'John Smith'}}}])
        file = open('pyThesaurus/tests/data/sample008.rdf')
        t = Thesaurus()
        io = SKOSCore.ioSKOSCore('en', thesaurus=t, contexts=[])
        io.read(file)
        self.assertEqualSets(t.get_publicNotes(t('zoology@en')[0])['scopenote'], [{'resource': 'http://www.example.com/notes/zoology.txt'}])
        file = open('pyThesaurus/tests/data/sample009.rdf')
        t = Thesaurus()
        io = SKOSCore.ioSKOSCore('en', thesaurus=t, contexts=[])
        io.read(file)
        self.assertEqualSets(t.get_publicNotes(t('botany@en')[0])['scopenote'], [{'document': {'language': {'value': 'EN', 'label': 'English'}, 'creator': {'person': {'mbox': 'mailto:jsmith@example.org', 'name': 'John Smith'}}}}])

    def testLoadSemanticRelationships(self):
        """
                |
                |
                |
                """
        file = open('pyThesaurus/tests/data/sample010.rdf')
        t = Thesaurus()
        io = SKOSCore.ioSKOSCore('en', thesaurus=t, contexts=[])
        io.read(file)
        self.assertEqual(t.get_broader('mammals@en', ['en']), ['animals@en'])
        self.assertEqual(t.get_narrower('animals@en', ['en']), ['mammals@en'])
        file = open('pyThesaurus/tests/data/sample011.rdf')
        t = Thesaurus()
        io = SKOSCore.ioSKOSCore('en', thesaurus=t, contexts=[])
        io.read(file)
        self.assertEqualSets(t.get_related('birds@en', ['en'], exclude=True), ['ornithology@en'])
        self.assertEqualSets(t.get_related('birds@en', ['en'], exclude=False), ['birds@en', 'ornithology@en'])
        self.assertEqualSets(t.get_related('ornithology@en', ['en'], exclude=True), ['birds@en'])

    def _testLoadMeaningfulCollectionsOfConcepts(self):
        """
                |
                |
                |
                """
        file = open('pyThesaurus/tests/data/sample012.rdf')
        t = SKOSCore.load(file, 'en')
        file = open('pyThesaurus/tests/data/sample013.rdf')
        t = SKOSCore.load(file, 'en')
        file = open('pyThesaurus/tests/data/sample014.rdf')
        t = Thesaurus()
        io = SKOSCore.ioSKOSCore('en', thesaurus=t, contexts=[])
        io.read(file)
        file = open('pyThesaurus/tests/data/sample015.rdf')
        t = Thesaurus()
        io = SKOSCore.ioSKOSCore('en', thesaurus=t, contexts=[])
        io.read(file)
        file = open('pyThesaurus/tests/data/sample016.rdf')
        t = Thesaurus()
        io = SKOSCore.ioSKOSCore('en', thesaurus=t, contexts=[])
        io.read(file)

    def _testLoadConceptSchemes(self):
        """
                |
                |
                |
                """
        file = open('pyThesaurus/tests/data/sample017.rdf')
        t = Thesaurus()
        io = SKOSCore.ioSKOSCore('en', thesaurus=t, contexts=[])
        io.read(file)
        self.assertEqualSet(t.schemes(), [''])

    def _testLoadSubjectIndexing(self):
        pass

    def _testLoadSubjectIndexing(self):
        pass

    def _testLoadPublishedSubjectIndicators(self):
        pass

    def _testLoadOpenIssues(self):
        pass

    def testLoadRealFile(self):
        file = open('pyThesaurus/tests/data/ukat_concepts.rdf')
        t = Thesaurus()
        io = SKOSCore.ioSKOSCore('en', thesaurus=t, contexts=[])
        io.read(file)
        self.assertEqualSets(t.get_narrower('Educational sciences and environment@en', ['en']), [
         'Education and skills@en', 'Education@en', 'Educational environment@en', 'Educational sciences@en', 'Girls education@en', 'ICT education at school@en', 'Information and communication technologies education at school@en', 'Labor unions and education@en', 'Learning and scholarship@en', 'Learning environment@en', 'Learning@en', 'Libraries and education@en', 'Medieval education@en', 'Pedagogy@en', 'Socialism and education@en', 'Sound recordings in education@en', 'Studies@en', 'Study and teaching@en', 'Trade unions and education@en', 'Volunteer workers in education@en', 'Womens education@en'])
        self.assertEqualSets(t.get_broader('Educational sciences and environment@en', ['en']), [])
        self.assertEqualSets(t.get_narrower('Educational policy@en', ['en']), [
         'Adult literacy@en', 'Advancement of education@en', 'Alternative education@en', 'Anticurriculum movement@en', 'Business links with schools@en', 'Church and college@en', 'Church and education@en', 'Community and education@en', 'Community links with schools@en', 'Computer uses in education@en', 'Computers for learning applications@en', 'Deschooling@en', 'Education and culture@en', 'Education and state@en', 'Educational aims@en', 'Educational alternatives@en', 'Educational computing@en', 'Educational development@en', 'Educational discrimination@en', 'Educational goals@en', 'Educational objectives@en', 'Educational policy@en', 'Educational strategies@en', 'Higher education and state@en', 'Industry and education@en', 'International cooperation education@en', 'International education@en', 'International understanding education@en', 'Language of instruction@en', 'Leisure and education@en', 'Leisure education@en', 'Right to education@en', 'Role of education@en', 'School industry relationship@en', 'State and education@en', 'Study abroad@en', 'Training abroad@en', 'Transnational education@en', 'Values education@en'])
        self.assertEqualSets(t.get_broader('Educational policy@en', ['en']), [])
        self.assertEqualSets(t.get_narrower('Poems@en', ['en']), [])
        self.assertEqualSets(t.get_broader('Poems@en', ['en']), [
         'Basque poetry@en', 'Belgian poetry (French)@en', 'Breton poetry@en', 'Chinese poetry@en', 'English dialect poetry@en', 'English poems@en', 'English poetry@en', 'English prose poems@en', 'French poetry@en', 'German poetry@en', 'Greek poetry@en', 'Irish poetry@en', 'Italian poetry@en', 'Latin poetry@en', 'Medieval poetry@en', 'Middle English poetry@en', 'Persian poetry@en', 'Poetry@en', 'Russian poetry@en', 'Scottish poetry@en', 'Spanish poetry@en', 'Verse@en', 'Welsh poetry@en'])

    def _LoadSaveRealFile(self, file):
        i = open(file)
        t = Thesaurus()
        io = SKOSCore.ioSKOSCore('en', thesaurus=t, contexts=[])
        io.read(i)
        i.close()
        o = open('pyThesaurus/tests/data/outtest.rdf', 'w')
        io.write(o)
        o.close()
        i = open('pyThesaurus/tests/data/outtest.rdf')
        t = Thesaurus()
        io = SKOSCore.ioSKOSCore('en', thesaurus=t, contexts=[])
        io.read(i)
        i.close()
        return t

    def testSaveRealFile(self):
        t = self._LoadSaveRealFile('pyThesaurus/tests/data/sample000.rdf')
        self.assertEqual(t.get_prefered('animals@en', ['en']), ['animals@en'])
        self.assertEqual(t.get_prefered('creatures@en', ['en']), ['animals@en'])
        self.assertEqual(t.get_prefered('fauna@en', ['en']), ['animals@en'])
        self.assertEqual(t.get_prefered('fauna@en', ['fr']), [])
        t = self._LoadSaveRealFile('pyThesaurus/tests/data/sample001.rdf')
        self.assertEqual(t.get_prefered('wetness@en', ['en']), ['wetness@en'])
        self.assertEqual(t.get_prefered('dryness@en', ['en']), ['wetness@en'])
        self.assertEqual(t.get_prefered('shrubs@en', ['en']), ['shrubs@en'])
        self.assertEqual(t.get_prefered('bushes@en', ['en']), ['shrubs@en'])
        self.assertEqual(t.get_prefered('granite@en', ['en']), ['rocks@en'])
        self.assertEqual(t('rocks@en'), t('basalt@en'))
        self.assertEqual(t('granite@en'), t('slate@en'))
        self.assertEqual(t('basalt@en'), t('slate@en'))
        t = self._LoadSaveRealFile('pyThesaurus/tests/data/sample002.rdf')
        self.assertEqual(t('abattoirs@en'), t('abattoirs@en'))
        self.assertEqual(t('abatoirs@en'), t('abattoirs@en'))
        self.assertEqual(t('abbatoirs@en'), t('abattoirs@en'))
        self.assertEqual(t('abbattoirs@en'), t('abattoirs@en'))
        self.assertEqualSets(t.get_equivalent('abbattoirs@en', ['es', 'en']), ['abattoirs@en'])
        t = self._LoadSaveRealFile('pyThesaurus/tests/data/sample003.rdf')
        self.assertEqual(t('shrubs@en'), t('shrubs@en'))
        self.assertEqual(t('bushes@en'), t('shrubs@en'))
        self.assertEqual(t('arbuste@fr'), t('shrubs@en'))
        self.assertEqual(t('buisson@fr'), t('shrubs@en'))
        self.assertEqualSets(t.get_prefered('buisson@fr', ['fr', 'en']), ['shrubs@en', 'arbuste@fr'])
        self.assertEqualSets(t.get_prefered('buisson@fr', ['en']), ['shrubs@en'])
        self.assertEqualSets(t.get_prefered('buisson@fr', ['fr']), ['arbuste@fr'])
        t = self._LoadSaveRealFile('pyThesaurus/tests/data/sample004.rdf')
        self.warning('prefSymbol, altSymbol are not implemented in this version')
        if True:
            t = self._LoadSaveRealFile('pyThesaurus/tests/data/sample005.rdf')
            self.assertEqualSets(t.get_prefered('banana republic@en', 'en'), ['banana republic@en'])
            self.assertEqualSets(t('banana republic@en'), [0])
            self.assertEqual(t.get_publicNotes(t('banana republic@en')[0])['definition'][0], 'A small country, especially in South and Central America, that is\n\t\tpoor and often badly and immorally ruled.@en')
            t = self._LoadSaveRealFile('pyThesaurus/tests/data/sample006.rdf')
            self.assertEqualSets(t.get_prefered('pineapples@en', 'fr'), ['ananas@fr'])
            self.assertEqualSets(t.get_publicNotes(t('pineapples@en')[0])['definition'], [
             unicode('The fruit of plants of the family Bromeliaceae.@en', 'latin1'), unicode(b'Le fruit de la plante herbac\xe9e de la famille des brom\xe9liac\xe9es.@fr', 'latin1')])
            t = self._LoadSaveRealFile('pyThesaurus/tests/data/sample007.rdf')
            self.assertEqualSets(t.get_publicNotes(t('notebook computers@en')[0])['changenote'], [{'value': "The preferred label for this concept changed from 'laptop computers' to 'notebook computers' on 23 Jan 1999.", 'creator': {'person': {'mbox': 'mailto:jsmith@example.org', 'name': 'John Smith'}}}])
            t = self._LoadSaveRealFile('pyThesaurus/tests/data/sample008.rdf')
            self.assertEqualSets(t.get_publicNotes(t('zoology@en')[0])['scopenote'], [{'resource': 'http://www.example.com/notes/zoology.txt'}])
            t = self._LoadSaveRealFile('pyThesaurus/tests/data/sample009.rdf')
            self.assertEqualSets(t.get_publicNotes(t('botany@en')[0])['scopenote'], [{'document': {'language': {'value': 'EN', 'label': 'English'}, 'creator': {'person': {'mbox': 'mailto:jsmith@example.org', 'name': 'John Smith'}}}}])
        if True:
            t = self._LoadSaveRealFile('pyThesaurus/tests/data/sample010.rdf')
            self.assertEqual(t.get_broader('mammals@en', ['en']), ['animals@en'])
            self.assertEqual(t.get_narrower('animals@en', ['en']), ['mammals@en'])
            t = self._LoadSaveRealFile('pyThesaurus/tests/data/sample011.rdf')
            self.assertEqualSets(t.get_related('birds@en', ['en'], exclude=True), ['ornithology@en'])
            self.assertEqualSets(t.get_related('birds@en', ['en'], exclude=False), ['birds@en', 'ornithology@en'])
            self.assertEqualSets(t.get_related('ornithology@en', ['en'], exclude=True), ['birds@en'])
        if False:
            t = self._LoadSaveRealFile('pyThesaurus/tests/data/sample012.rdf')
            t = SKOSCore.load(file, 'en')
            t = self._LoadSaveRealFile('pyThesaurus/tests/data/sample013.rdf')
            t = SKOSCore.load(file, 'en')
            t = self._LoadSaveRealFile('pyThesaurus/tests/data/sample014.rdf')
            t = SKOSCore.load(file, 'en')
            t = self._LoadSaveRealFile('pyThesaurus/tests/data/sample015.rdf')
            t = SKOSCore.load(file, 'en')
            t = self._LoadSaveRealFile('pyThesaurus/tests/data/sample016.rdf')
            t = SKOSCore.load(file, 'en')
        if False:
            t = self._LoadSaveRealFile('pyThesaurus/tests/data/sample017.rdf')
            t = SKOSCore.load(file, 'en')


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(testSKOSCore))
    return suite


if __name__ == '__main__':
    unittest.main()