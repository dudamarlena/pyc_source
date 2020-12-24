# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/collective/kssinline/browser/views/foldercontents.py
# Compiled at: 2008-10-02 13:12:26
from zope.interface import implements
from plone.app.content.browser.interfaces import IFolderContentsView
from plone.app.content.browser import foldercontents
from tableview import Table

class FolderContentsView(foldercontents.FolderContentsView):
    """
    """
    __module__ = __name__
    implements(IFolderContentsView)

    def contents_table(self):
        table = FolderContentsTable(self.context, self.request)
        return table.render()


class FolderContentsTable(foldercontents.FolderContentsTable):
    __module__ = __name__

    def __init__(self, context, request, contentFilter={}):
        foldercontents.FolderContentsTable.__init__(self, context, request, contentFilter)
        url = self.context.absolute_url()
        view_url = url + '/@@folder_contents'
        self.table = Table(request, url, view_url, self.items, show_sort_column=self.show_sort_column, buttons=self.buttons, context=context)


class FolderContentsKSSView(foldercontents.FolderContentsKSSView):
    __module__ = __name__
    table = FolderContentsTable