# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-ppc/egg/plonetheme/terrafirma/browser/author_link.py
# Compiled at: 2008-05-03 14:29:09
from plone.app.layout.viewlets.common import ViewletBase
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

class AuthorLinkViewlet(ViewletBase):
    __module__ = __name__
    render = ViewPageTemplateFile('author_link.pt')

    def update(self):
        super(AuthorLinkViewlet, self).update()