# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-i386/egg/Products/LinguaFace/browser/foldercontents.py
# Compiled at: 2010-11-30 09:59:25
from plone.app.content.browser.foldercontents import FolderContentsView as BaseFolderContentsView
from plone.app.content.browser.foldercontents import FolderContentsKSSView as BaseFolderContentsKSSView
from plone.app.content.browser.foldercontents import FolderContentsTable

class FolderContentsView(BaseFolderContentsView):
    """
    """
    __module__ = __name__

    def contents_table(self):
        table = FolderContentsTable(self.context, self.request, contentFilter={'getPhysicalTree': True})
        return table.render()


class FolderContentsKSSView(BaseFolderContentsKSSView):
    __module__ = __name__

    def update_table(self, pagenumber='1', sort_on='getObjPositionInParent', sort_order='', show_all=False):
        self.request.set('sort_on', sort_on)
        if sort_order:
            self.request.set('sort_order', sort_order)
        self.request.set('pagenumber', pagenumber)
        table = self.table(self.context, self.request, contentFilter={'sort_on': sort_on, 'sort_order': sort_order, 'getPhysicalTree': True})
        core = self.getCommandSet('core')
        core.replaceHTML('#folderlisting-main-table', table.render())
        return self.render()