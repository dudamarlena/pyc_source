# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/plonetheme/notredame/browser/viewlets.py
# Compiled at: 2009-03-31 16:25:00
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets import common

class PathBarViewlet(common.PathBarViewlet):
    """Customized breadcrumbs class
    """
    __module__ = __name__
    render = ViewPageTemplateFile('templates/pathbar.pt')