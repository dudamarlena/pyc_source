# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/simpleweb/test/test_dispatcher.py
# Compiled at: 2007-01-10 11:06:17
import dispatcher

def GET():
    return 'GET'


class TestUrls(object):
    __module__ = __name__

    def test_add(self):
        urls = dispatcher.Urls()
        urls.add('/', 'test_dispatcher')
        urls.add('/foo', 'foo.bar.noexist')
        assert ('/', 'test_dispatcher') in urls.urlmap
        assert ('/foo', 'foo.bar.noexist') in urls.urlmap

    def test_geturls(self):
        urls = dispatcher.Urls()
        urls.add('/', 'test_dispatcher')
        myurls = urls.geturls()
        print myurls.mappings
        assert myurls.mappings[0][1]['GET']