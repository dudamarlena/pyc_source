# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyThesaurus/tests/test_heavy.py
# Compiled at: 2008-10-06 10:31:21
import unittest, pyThesaurus.ioSKOSCore as SKOSCore
from pyThesaurus.Thesaurus import Thesaurus
from pyThesaurus.Concept import Concept

class testHeavy(unittest.TestCase):
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

    def _testSearchTerm(self):
        f = open('pyThesaurus/tests/data/ukat_concepts.rdf')
        t = SKOSCore.load(f, 'en')
        self.assertEqualSets(t.search_term('physiology'), ['Circulatory and respiratory physiology@en', 'Electrophysiology@en', 'Fatigue (physiology)@en', 'Height (physiology)@en', 'Human physiology@en', 'Musculoskeletal physiology@en', 'Neurophysiology@en', 'Plant physiology@en', 'Psychophysiology@en', 'Stress (physiology)@en', 'Weight (physiology)@en'])

    def _testContext(self):
        f = open('pyThesaurus/tests/data/ukat_concepts.rdf')
        t = SKOSCore.load(f, 'en')
        self.assertEqualSets(t.contexts(), ['http://www.ukat.org.uk/thesaurus', 'http://www.ukat.org.uk/thesaurus/micro/105', 'http://www.ukat.org.uk/thesaurus/micro/110', 'http://www.ukat.org.uk/thesaurus/micro/115', 'http://www.ukat.org.uk/thesaurus/micro/120', 'http://www.ukat.org.uk/thesaurus/micro/125', 'http://www.ukat.org.uk/thesaurus/micro/130', 'http://www.ukat.org.uk/thesaurus/micro/135', 'http://www.ukat.org.uk/thesaurus/micro/140', 'http://www.ukat.org.uk/thesaurus/micro/145', 'http://www.ukat.org.uk/thesaurus/micro/150', 'http://www.ukat.org.uk/thesaurus/micro/155', 'http://www.ukat.org.uk/thesaurus/micro/160', 'http://www.ukat.org.uk/thesaurus/micro/165', 'http://www.ukat.org.uk/thesaurus/micro/170', 'http://www.ukat.org.uk/thesaurus/micro/205', 'http://www.ukat.org.uk/thesaurus/micro/210', 'http://www.ukat.org.uk/thesaurus/micro/215', 'http://www.ukat.org.uk/thesaurus/micro/220', 'http://www.ukat.org.uk/thesaurus/micro/225', 'http://www.ukat.org.uk/thesaurus/micro/230', 'http://www.ukat.org.uk/thesaurus/micro/235', 'http://www.ukat.org.uk/thesaurus/micro/240', 'http://www.ukat.org.uk/thesaurus/micro/245', 'http://www.ukat.org.uk/thesaurus/micro/250', 'http://www.ukat.org.uk/thesaurus/micro/255', 'http://www.ukat.org.uk/thesaurus/micro/260', 'http://www.ukat.org.uk/thesaurus/micro/265', 'http://www.ukat.org.uk/thesaurus/micro/270', 'http://www.ukat.org.uk/thesaurus/micro/275', 'http://www.ukat.org.uk/thesaurus/micro/280', 'http://www.ukat.org.uk/thesaurus/micro/285', 'http://www.ukat.org.uk/thesaurus/micro/305', 'http://www.ukat.org.uk/thesaurus/micro/310', 'http://www.ukat.org.uk/thesaurus/micro/315', 'http://www.ukat.org.uk/thesaurus/micro/320', 'http://www.ukat.org.uk/thesaurus/micro/325', 'http://www.ukat.org.uk/thesaurus/micro/330', 'http://www.ukat.org.uk/thesaurus/micro/335', 'http://www.ukat.org.uk/thesaurus/micro/340', 'http://www.ukat.org.uk/thesaurus/micro/345', 'http://www.ukat.org.uk/thesaurus/micro/350', 'http://www.ukat.org.uk/thesaurus/micro/355', 'http://www.ukat.org.uk/thesaurus/micro/360', 'http://www.ukat.org.uk/thesaurus/micro/365', 'http://www.ukat.org.uk/thesaurus/micro/405', 'http://www.ukat.org.uk/thesaurus/micro/410', 'http://www.ukat.org.uk/thesaurus/micro/415', 'http://www.ukat.org.uk/thesaurus/micro/420', 'http://www.ukat.org.uk/thesaurus/micro/425', 'http://www.ukat.org.uk/thesaurus/micro/430', 'http://www.ukat.org.uk/thesaurus/micro/435', 'http://www.ukat.org.uk/thesaurus/micro/440', 'http://www.ukat.org.uk/thesaurus/micro/445', 'http://www.ukat.org.uk/thesaurus/micro/450', 'http://www.ukat.org.uk/thesaurus/micro/505', 'http://www.ukat.org.uk/thesaurus/micro/510', 'http://www.ukat.org.uk/thesaurus/micro/515', 'http://www.ukat.org.uk/thesaurus/micro/520', 'http://www.ukat.org.uk/thesaurus/micro/525', 'http://www.ukat.org.uk/thesaurus/micro/530', 'http://www.ukat.org.uk/thesaurus/micro/535', 'http://www.ukat.org.uk/thesaurus/micro/540', 'http://www.ukat.org.uk/thesaurus/micro/545', 'http://www.ukat.org.uk/thesaurus/micro/605', 'http://www.ukat.org.uk/thesaurus/micro/610', 'http://www.ukat.org.uk/thesaurus/micro/615', 'http://www.ukat.org.uk/thesaurus/micro/620', 'http://www.ukat.org.uk/thesaurus/micro/625', 'http://www.ukat.org.uk/thesaurus/micro/630', 'http://www.ukat.org.uk/thesaurus/micro/635', 'http://www.ukat.org.uk/thesaurus/micro/640', 'http://www.ukat.org.uk/thesaurus/micro/645', 'http://www.ukat.org.uk/thesaurus/micro/650', 'http://www.ukat.org.uk/thesaurus/micro/655', 'http://www.ukat.org.uk/thesaurus/micro/660', 'http://www.ukat.org.uk/thesaurus/micro/665', 'http://www.ukat.org.uk/thesaurus/micro/670', 'http://www.ukat.org.uk/thesaurus/micro/675', 'http://www.ukat.org.uk/thesaurus/micro/680', 'http://www.ukat.org.uk/thesaurus/micro/685', 'http://www.ukat.org.uk/thesaurus/micro/805', 'http://www.ukat.org.uk/thesaurus/micro/810', 'http://www.ukat.org.uk/thesaurus/micro/815'])
        self.assertEqual(len(t.get_terms_of_context('http://www.ukat.org.uk/thesaurus/micro/110')), 42)
        self.assertEqualSets(t.get_terms_of_context('http://www.ukat.org.uk/thesaurus/micro/110'), [['Access to education@en'], ['Adult literacy@en'], ['Alternative education@en', 'Anticurriculum movement@en', 'Deschooling@en', 'Educational alternatives@en'], ['Bilingual education@en'], ['Choice of school@en', 'Choosing a school@en', 'School choice and admission@en', 'School preferences@en', 'School types and choosing a school@en', 'Selection of schools@en'], ['Church and education@en', 'Church and college@en'], ['Community and education@en', 'Community links with schools@en'], ['Compulsory education@en'], ['Computer uses in education@en', 'Computers for learning applications@en', 'Educational computing@en'], ['Curriculum development@en', 'Curriculum design@en', 'Curriculum improvement@en', 'Curriculum innovation@en', 'Curriculum planning@en', 'Curriculum reform@en', 'Curriculum reorganization@en'], ['Democratization of education@en'], ['Diversification of education@en'], ['Education action zones@en'], ['Education and culture@en'], ['Educational development@en', 'Advancement of education@en'], ['Educational discrimination@en'], ['Educational experiments@en', 'Experimental education@en'], ['Educational innovations@en'], ['Educational objectives@en', 'Educational aims@en', 'Educational goals@en', 'Role of education@en'], ['Educational opportunities@en', 'Sexual discrimination (education opportunities)@en'], ['Educational policy@en'], ['Educational priority areas@en'], ['Educational reform@en', 'Educational change@en', 'Educational renewal@en'], ['Educational strategies@en'], ['Educational trends@en'], ['Enrolment trends@en'], ['Free education@en'], ['Functional illiteracy@en'], ['Illiteracy@en'], ['Industry and education@en', 'Business links with schools@en', 'School industry relationship@en'], ['Intercultural education@en', 'Bicultural education@en', 'Crosscultural education@en', 'Multicultural education@en'], ['International education@en', 'International cooperation education@en', 'International understanding education@en', 'Values education@en'], ['Language of instruction@en'], ['Leisure and education@en', 'Leisure education@en'], ['Mission administration@en'], ['Mission policy@en'], ['Right to education@en'], ['School integration@en', 'Educational integration@en', 'School desegregation@en', 'School segregation@en'], ['State and education@en', 'Education and state@en', 'Higher education and state@en'], ['Study abroad@en', 'Training abroad@en', 'Transnational education@en'], ['Teaching method innovations@en'], ['Universal education@en', 'Educational equalization@en', 'Equal education@en', 'Equal opportunity (education)@en']])
        self.assertEqualSets(t.get_equivalent('Agriculture@en', ['en'], contexts=['http://www.ukat.org.uk/thesaurus/micro/635']), [
         'Agricultural grants@en', 'Agriculture and state@en', 'Agriculture and the state@en', 'Agriculture, environment and natural resources@en', 'Agriculture@en', 'Arable husbandry operations@en', 'Arable husbandry@en'])
        self.assertEqualSets(t.get_similars('Agriculture@en', ['en'], contexts=['http://www.ukat.org.uk/thesaurus/micro/635']), [])
        self.assertEqualSets(t.get_broader('Agriculture@en', ['en'], contexts=['http://www.ukat.org.uk/thesaurus/micro/635']), [])
        self.assertEqualSets(t.get_narrower('Agriculture@en', ['en'], contexts=['http://www.ukat.org.uk/thesaurus/micro/635']), [
         'Agricultural chemistry@en', 'Agricultural engineering@en', 'Agricultural practices@en', 'Agricultural research@en', 'Agriculture (farming)@en', 'Farming@en', 'Husbandry@en', 'Ranching@en'])
        self.assertEqualSets(t.get_related('Agriculture@en', ['en'], contexts=['http://www.ukat.org.uk/thesaurus/micro/635']), [
         'Agricultural biology@en', 'Agroclimatology@en', 'Agronomy@en', 'Animal breeding (farm)@en', 'Animal husbandry@en', 'Animal production@en', 'Cropping systems@en', 'Cultivation systems@en', 'Cultivation@en', 'Farmers@en', 'Farming systems@en', 'Forestry and community@en', 'Forestry@en', 'Forests and forestry@en', 'Livestock farming@en', 'State of cultivation@en', 'Stock farming@en'])


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(testHeavy))
    return suite


if __name__ == '__main__':
    unittest.main()