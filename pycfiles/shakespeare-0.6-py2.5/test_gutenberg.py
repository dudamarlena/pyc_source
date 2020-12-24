# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/rgrp/svnroot/shakespeare/trunk/shksprdata/getdata/test_gutenberg.py
# Compiled at: 2008-09-13 09:24:33
import shakespeare
shakespeare.register_config('test.ini')
import shakespeare.cache, shksprdata.getdata.gutenberg as GG, shakespeare.gutenberg

class TestGutenbergIndex:
    gutindex = GG.GutenbergIndex(shakespeare.cache.default)

    def test_parse_line_for_folio(self):
        inStr = 'Jul 2000 Cymbeline, by Wm. Shakespeare  [First Folio]=[FF] [0ws39xxx.xxx] 2269'
        out = self.gutindex.parse_line_for_folio(inStr)
        exp = ['Cymbeline', '2000', '0ws39']
        for ii in range(len(exp)):
            assert out[ii] == exp[ii]

    def test_parse_line_for_normal(self):
        inStr = 'Nov 1998 Cymbeline, by William Shakespeare [2ws39xxx.xxx] 1538'
        out = self.gutindex.parse_line_for_normal(inStr)
        exp = ['Cymbeline', '1998', '2ws39']
        for ii in range(len(exp)):
            assert out[ii] == exp[ii]

    def test_parse_line_for_normal_2(self):
        """Added after discovering that Othello was not getting picked up."""
        inStr = 'Nov 1998 Othello, by Shakespeare [2ws32xxx.xxx] 1531'
        out = self.gutindex.parse_line_for_normal(inStr)
        print out
        exp = ['Othello', '1998', '2ws32']
        for ii in range(len(exp)):
            assert out[ii] == exp[ii]

    def test_get_relevant_works(self):
        works = self.gutindex.get_relevant_works()
        assert len(works) == 77


import shakespeare.model

class TestHelper:

    @classmethod
    def setup_class(self):
        self.url1 = 'http://www.gutenberg.org/dirs/etext00/0ws2510.txt'
        self.url2 = 'http://www.gutenberg.org/dirs/etext98/2ws2510.txt'
        cache = shakespeare.cache.default
        works = GG.GutenbergIndex(cache).get_relevant_works()
        self.helper = GG.Helper(works, cache)

    def test_clean(self):
        line = '%s %s' % (self.url1, self.url2)
        self.helper.clean(line)

    def test_title_to_name(self):
        inlist = [
         'King Henry VIII',
         'The Merchant of Venice',
         'Twelfth Night',
         "All's Well That Ends Well"]
        explist = [
         'henry_viii',
         'merchant_of_venice',
         'twelfth_night',
         'alls_well_that_ends_well']
        for ii in range(len(inlist)):
            assert explist[ii] == self.helper.title_to_name(inlist[ii])

    def test_add_to_db(self):
        self.helper.add_to_db()
        text1 = shakespeare.model.Material.byName('hamlet_gut')
        shakespeare.model.Material.byName('hamlet_gut_f')
        assert 'Shakespeare, William' == text1.creator
        alltexts = shakespeare.model.Material.query.all()

    def test_execute(self):
        self.helper.execute()