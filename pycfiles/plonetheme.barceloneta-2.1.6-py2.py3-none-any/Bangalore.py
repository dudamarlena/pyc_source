# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/plonetheme/Bangalore/browser/Bangalore.py
# Compiled at: 2010-02-05 09:52:09
from plone.app.layout.viewlets.common import PathBarViewlet
from plone.app.layout.links.viewlets import FaviconViewlet
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

class BangalorePathBar(PathBarViewlet):
    __module__ = __name__
    render = ViewPageTemplateFile('templates/bgl_path_bar.pt')


class BangaloreFavicon(FaviconViewlet):
    __module__ = __name__
    render = ViewPageTemplateFile('templates/favicon.pt')