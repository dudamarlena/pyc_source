# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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