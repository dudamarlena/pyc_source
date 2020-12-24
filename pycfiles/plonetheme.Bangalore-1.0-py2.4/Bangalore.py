# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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