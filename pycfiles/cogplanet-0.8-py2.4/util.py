# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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