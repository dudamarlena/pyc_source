# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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