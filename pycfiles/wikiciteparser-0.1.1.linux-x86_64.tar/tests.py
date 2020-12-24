# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/antonin/Programmation/OA/wikiciteparser/.virtualenv/lib/python2.7/site-packages/wikiciteparser/tests.py
# Compiled at: 2016-03-11 17:40:27
from __future__ import unicode_literals
import unittest
from .parser import *

class ParsingTests(unittest.TestCase):

    def test_multiple_authors(self):
        p = parse_citation_dict({b'doi': b'10.1111/j.1365-2486.2008.01559.x', b'title': b"Climate change, plant migration, and range collapse in a global biodiversity hotspot: the ''Banksia'' (Proteaceae) of Western Australia", b'issue': b'6', b'journal': b'Global Change Biology', b'year': b'2008', b'volume': b'14', b'last4': b'Dunn', b'last1': b'Fitzpatrick', b'last3': b'Sanders', b'last2': b'Gove', b'first1': b'Matthew C.', b'first2': b'Aaron D.', b'first3': b'Nathan J.', b'first4': b'Robert R.', b'pages': b'1–16'}, template_name=b'cite journal')
        self.assertEqual(p[b'Authors'], [{b'last': b'Fitzpatrick', b'first': b'Matthew C.'}, {b'last': b'Gove', b'first': b'Aaron D.'}, {b'last': b'Sanders', b'first': b'Nathan J.'}, {b'last': b'Dunn', b'first': b'Robert R.'}])

    def test_vauthors(self):
        p = parse_citation_dict({b'doi': b'10.1016/s1097-2765(00)80111-2', b'title': b'SAP30, a component of the mSin3 corepressor complex involved in N-CoR-mediated repression by specific transcription factors', b'journal': b'Mol. Cell', b'volume': b'2', b'date': b'July 1998', b'pmid': b'9702189', b'issue': b'1', b'pages': b'33–42', b'vauthors': b'Laherty CD, Billin AN, Lavinsky RM, Yochum GS, Bush AC, Sun JM, Mullen TM, Davie JR, Rose DW, Glass CK, Rosenfeld MG, Ayer DE, Eisenman RN'}, template_name=b'cite journal')
        self.assertEqual(p[b'Authors'], [{b'last': b'Laherty', b'first': b'CD'}, {b'last': b'Billin', b'first': b'AN'}, {b'last': b'Lavinsky', b'first': b'RM'}, {b'last': b'Yochum', b'first': b'GS'}, {b'last': b'Bush', b'first': b'AC'}, {b'last': b'Sun', b'first': b'JM'}, {b'last': b'Mullen', b'first': b'TM'}, {b'last': b'Davie', b'first': b'JR'}, {b'last': b'Rose', b'first': b'DW'}, {b'last': b'Glass', b'first': b'CK'}, {b'last': b'Rosenfeld', b'first': b'MG'}, {b'last': b'Ayer', b'first': b'DE'}, {b'last': b'Eisenman', b'first': b'RN'}])

    def test_remove_links(self):
        p = parse_citation_dict({b'title': b'Mobile, Alabama', b'url': b'http://archive.org/stream/ballouspictorial1112ball#page/408/mode/2up', b'journal': b"[[Ballou's Pictorial Drawing-Room Companion]]", b'volume': b'12', b'location': b'Boston', b'date': b'June 27, 1857'}, template_name=b'cite journal')
        self.assertEqual(p[b'Periodical'], b"Ballou's Pictorial Drawing-Room Companion")

    def test_authorlink(self):
        p = parse_citation_dict({b'publisher': b'[[World Bank]]', b'isbn': b'978-0821369418', b'title': b'Performance Accountability and Combating Corruption', b'url': b'http://siteresources.worldbank.org/INTWBIGOVANTCOR/Resources/DisruptingCorruption.pdf', b'page': b'309', b'last1': b'Shah', b'location': b'[[Washington, D.C.]], [[United States|U.S.]]', b'year': b'2007', b'first1': b'Anwar', b'authorlink1': b'Anwar Shah', b'oclc': b'77116846'}, template_name=b'citation')
        self.assertEqual(p[b'Authors'], [{b'link': b'Anwar Shah', b'last': b'Shah', b'first': b'Anwar'}])

    def test_unicode(self):
        p = parse_citation_dict({b'title': b'Дороги царей (Roads of Emperors)', b'url': b'http://magazines.russ.ru/ural/2004/10/mar11.html', b'journal': b'Урал', b'author': b'Margovenko, A', b'volume': b'10', b'year': b'2004'}, template_name=b'cite journal')
        self.assertEqual(p[b'Title'], b'Дороги царей (Roads of Emperors)')

    def test_mwtext(self):
        import mwparserfromhell
        mwtext = b'\n        ===Articles===\n        * {{Citation | last1=Lambek | first1=Joachim | author1-link=Joachim Lambek | last2=Moser | first2=L. | title=Inverse and Complementary Sequences of Natural Numbers| doi=10.2307/2308078 | mr=0062777  | journal=[[American Mathematical Monthly|The American Mathematical Monthly]] | issn=0002-9890 | volume=61 | issue=7 | pages=454–458 | year=1954 | jstor=2308078 | publisher=The American Mathematical Monthly, Vol. 61, No. 7}}\n        * {{Citation | last1=Lambek | first1=J. | author1-link=Joachim Lambek | title=The Mathematics of Sentence Structure | year=1958 | journal=[[American Mathematical Monthly|The American Mathematical Monthly]] | issn=0002-9890 | volume=65 | pages=154–170 | doi=10.2307/2310058 | issue=3 | publisher=The American Mathematical Monthly, Vol. 65, No. 3 | jstor=1480361}}\n        *{{Citation | last1=Lambek | first1=Joachim | author1-link=Joachim Lambek | title=Bicommutators of nice injectives | doi=10.1016/0021-8693(72)90034-8 | mr=0301052  | year=1972 | journal=Journal of Algebra | issn=0021-8693 | volume=21 | pages=60–73}}\n        *{{Citation | last1=Lambek | first1=Joachim | author1-link=Joachim Lambek | title=Localization and completion | doi=10.1016/0022-4049(72)90011-4 | mr=0320047  | year=1972 | journal=Journal of Pure and Applied Algebra | issn=0022-4049 | volume=2 | pages=343–370 | issue=4}}\n        *{{Citation | last1=Lambek | first1=Joachim | author1-link=Joachim Lambek | title=A mathematician looks at Latin conjugation | mr=589163  | year=1979 | journal=Theoretical Linguistics | issn=0301-4428 | volume=6 | issue=2 | pages=221–234 | doi=10.1515/thli.1979.6.1-3.221}}\n\n        '
        wikicode = mwparserfromhell.parse(mwtext)
        for tpl in wikicode.filter_templates():
            parsed = parse_citation_template(tpl)
            print parsed
            self.assertIsInstance(parsed, dict)