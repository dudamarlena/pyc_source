# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/redomino/advancedkeyword/browser/viewlets.py
# Compiled at: 2013-05-08 04:41:18
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets.common import ViewletBase
from redomino.advancedkeyword.indexers import subjects_indexer

class KeywordsViewlet(ViewletBase):
    index = ViewPageTemplateFile('templates/keywords_viewlet.pt')

    def update(self):
        super(KeywordsViewlet, self).update()
        subjects = subjects_indexer(self.context)
        subjects.sort()
        self.subjects = subjects