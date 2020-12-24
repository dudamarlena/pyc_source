# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/shakespeare/tests/test_cache.py
# Compiled at: 2008-10-29 17:02:16
import os, shutil, tempfile, shakespeare.cache

class TestCache(object):

    @classmethod
    def setup_class(cls):
        cls.cache_path = tempfile.mkdtemp()
        cls.cache = shakespeare.cache.Cache(cls.cache_path)
        cls.url = 'http://www.gutenberg.org/dirs/GUTINDEX.ALL'
        cls.url2 = 'http://project.knowledgeforge.net/shakespeare/svn/trunk/CHANGELOG.txt'

    @classmethod
    def teardown_class(cls):
        shutil.rmtree(cls.cache_path)

    def test_path(self):
        exp = os.path.join(self.cache_path, self.url[7:])
        out = self.cache.path(self.url)
        assert out == exp

    def test_path_2(self):
        exp = os.path.join(self.cache_path, 'www.gutenberg.org/dirs/cleanedGUTINDEX.ALL')
        out = self.cache.path(self.url, 'cleaned')
        assert exp == out

    def test_download_url(self):
        exp = os.path.join(self.cache_path, self.url2[7:])
        self.cache.download_url(self.url2, overwrite=True)
        assert os.path.exists(exp)