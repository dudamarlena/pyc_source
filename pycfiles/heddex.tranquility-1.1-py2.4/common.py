# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/heddex/tranquility/browser/common.py
# Compiled at: 2009-06-04 17:33:35
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets.common import GlobalSectionsViewlet
from plone.app.layout.viewlets.common import PathBarViewlet

class themeGlobalSectionsViewlet(GlobalSectionsViewlet):
    __module__ = __name__
    index = ViewPageTemplateFile('sections.pt')


class themePathBarViewlet(PathBarViewlet):
    __module__ = __name__
    index = ViewPageTemplateFile('path_bar.pt')