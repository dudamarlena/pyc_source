# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\tests\unit\substitutions\test_bibliography.py
# Compiled at: 2016-09-30 14:50:44
# Size of source mod 2**32: 2144 bytes
from unittest import main
from tests.commons import FlapTest
from tests.latex_project import a_project

class BibliographyTests(FlapTest):

    def test_fetching_bibliography(self):
        self._assume = a_project().with_main_file('\\bibliography{biblio}').with_file('biblio.bib', 'some refereneces')
        self._expect = a_project().with_merged_file('\\bibliography{biblio}').with_file('biblio.bib', 'some refereneces')
        self._do_test_and_verify()

    def test_fetching_bibliography_stored_in_sub_directories(self):
        self._assume = a_project().with_main_file('\\bibliography{etc/biblio}').with_file('etc/biblio.bib', 'some refereneces')
        self._expect = a_project().with_merged_file('\\bibliography{etc_biblio}').with_file('etc_biblio.bib', 'some refereneces')
        self._do_test_and_verify()

    def test_interaction_with_graphicpath(self):
        self._assume = a_project().with_main_file('\\graphicspath{img}\\bibliography{parts/biblio}').with_file('parts/biblio.bib', 'some refereneces')
        self._expect = a_project().with_merged_file('\\bibliography{parts_biblio}').with_file('parts_biblio.bib', 'some refereneces')
        self._do_test_and_verify()


if __name__ == '__main__':
    main()