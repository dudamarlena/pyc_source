# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/freearch/theme/browser/path_bar.py
# Compiled at: 2008-06-18 05:21:29
from plone.app.layout.viewlets.common import PathBarViewlet
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

class FreeArchPathBarViewlet(PathBarViewlet):
    render = ViewPageTemplateFile('templates/path_bar.pt')