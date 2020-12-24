# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/jw/tustep/browser/viewlets.py
# Compiled at: 2010-01-28 06:18:31
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets.common import ViewletBase
from plone.app.layout.viewlets.content import DocumentActionsViewlet
from zope.component import getMultiAdapter
import datetime

class DatumText(ViewletBase):
    __module__ = __name__
    index = ViewPageTemplateFile('viewlet.pt')

    def update(self):
        super(DatumText, self).update()
        self.DatumJetzt = datetime.date.today()