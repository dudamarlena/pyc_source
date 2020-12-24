# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/shakespeare/tests/test_search.py
# Compiled at: 2008-10-29 17:02:17
import os, shutil, tempfile, StringIO, shakespeare.search, shakespeare.tests

class TestSearch:

    def setUp(self):
        self.text = shakespeare.tests.make_fixture()
        basetmp = tempfile.gettempdir()
        self.tmpdir = os.path.join(basetmp, 'openshkspr-search')
        if os.path.exists(self.tmpdir):
            shutil.rmtree(self.tmpdir)
        os.makedirs(self.tmpdir)
        self.index = shakespeare.search.SearchIndex(self.tmpdir)
        self.index.add_item(StringIO.StringIO(self.text.content), self.text.name)

    def test_add_item(self):
        assert self.index.get_database().get_doccount() > 0

    def test_remove_item(self):
        self.index.remove_item(self.text.name)
        assert self.index.get_database().get_doccount() == 0

    def test_search_1(self):
        out = self.index.search('summer')
        assert len(out) == 2
        mset1 = out[0]
        exp = "Shall I compare thee to a summer's day"
        assert mset1.document.get_data().startswith(exp)

    def test_search_2(self):
        out = self.index.search('summer')
        mset1 = out[1]
        exp = "But thy eternal summer shall not fade,\nNor lose possession of that fair thou ow'st,"
        assert mset1.document.get_data().startswith(exp)

    def test_search_3(self):
        out = self.index.search('rough')
        assert len(out) == 1

    def test_retrieve_lineno(self):
        out = self.index.search('summer')
        mset1 = out[1]
        lineno = mset1.document.get_value(shakespeare.search.LINE_NO)
        assert lineno == '9'

    def test_retrieve_itemid(self):
        out = self.index.search('summer')
        mset1 = out[1]
        name = mset1.document.get_value(shakespeare.search.ITEM_ID)
        assert name == self.text.name