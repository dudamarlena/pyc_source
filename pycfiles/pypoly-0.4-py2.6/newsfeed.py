# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pypoly/content/newsfeed.py
# Compiled at: 2011-02-16 12:53:02
import os, types, pypoly

class FeedItem(object):
    title = ''
    link = ''
    description = ''
    author = ''
    uid = ''
    guid = ''
    date = ''


class FeedChannel(list):
    title = ''
    link = ''
    description = ''
    category = ''
    copyright = ''
    image = ''
    language = ''
    docs = ''
    webmaster = ''
    pubdate = ''

    def __init__(self):
        self.title = ''
        self.link = ''
        self.description = ''
        self.image = None
        return


class FeedImage(object):
    url = ''
    title = ''
    link = ''


class Feed(list):
    _template = ''
    _content_type = 'application/rss+xml'
    image = None

    def __init__(self):
        pass

    def render(self):
        pypoly.http.response.headers['Content-Type'] = 'application/rss+xml'
        tpl = pypoly.template.load_xml(os.path.join('newsfeeds', self._template))
        return tpl.generate(channels=self).render()


class RSS_0_9(Feed):

    def __init__(self):
        self._template = 'rss_0_9.xml'


class RSS_1_0(Feed):

    def __init__(self):
        self._template = 'rss_1_0.xml'


class RSS_2_0(Feed):

    def __init__(self):
        self._template = 'rss_2_0.xml'