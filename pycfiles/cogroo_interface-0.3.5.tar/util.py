# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.darwin-8.8.0-Power_Macintosh/egg/cogplanet/util.py
# Compiled at: 2006-12-28 02:37:03
from cogplanet.model import *
from elementtree import ElementTree

def import_opml(opml):
    doc = ElementTree.parse(opml)
    feeds = []
    for outline in doc.findall('//outline'):
        feed = Feed()
        feed.htmlurl = outline.get('htmlUrl')
        feed.xmlurl = outline.get('xmlUrl')
        feed.name = outline.get('title')
        feeds.append(feed)
        print outline.get('xmlUrl')

    return feeds