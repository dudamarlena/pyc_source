# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/plonetheme/notredame/browser/viewlets.py
# Compiled at: 2009-03-31 16:25:00
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets import common

class PathBarViewlet(common.PathBarViewlet):
    """Customized breadcrumbs class
    """
    __module__ = __name__
    render = ViewPageTemplateFile('templates/pathbar.pt')