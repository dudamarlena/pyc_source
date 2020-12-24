# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.3-ppc/egg/plonetheme/terrafirma/browser/author_link.py
# Compiled at: 2008-05-03 14:29:09
from plone.app.layout.viewlets.common import ViewletBase
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

class AuthorLinkViewlet(ViewletBase):
    __module__ = __name__
    render = ViewPageTemplateFile('author_link.pt')

    def update(self):
        super(AuthorLinkViewlet, self).update()