# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/egnyte/tests/test_search.py
# Compiled at: 2017-03-15 09:46:43
from egnyte.tests.config import EgnyteTestCase
FILE_PATH = '/search/test1.txt'
FILE_CONTENT = 'Lorem ipsum'
SEARCH_QUERY = 'ipsum'

class TestSearch(EgnyteTestCase):

    def setUp(self):
        super(TestSearch, self).setUp()
        self.root_folder.create()
        self.filepath = self.root_folder.path + FILE_PATH

    def test_file_search(self):
        _file = self.egnyte.file(self.filepath)
        _file.upload(FILE_CONTENT)
        search_results = self.egnyte.search.files(SEARCH_QUERY)
        self.assertIsNotNone(search_results)
        if search_results:
            self.assert_(SEARCH_QUERY in search_results[0].snippet)