# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/c2/patch/effectivedateforlisting/monkey.py
# Compiled at: 2010-01-30 03:43:31
__doc__ = '\nmonkey.py\n\nCreated by Manabu Terada on 2010-01-30.\nCopyright (c) 2010 CMScom. All rights reserved.\n'
from Acquisition import aq_inner
from plone.app.content.browser.foldercontents import FolderContentsTable
from plone.app.content.browser.foldercontents import FolderContentsView
from logging import getLogger
logger = getLogger(__name__)
info = logger.info

def contents_table(self):
    table = FolderContentsTable(aq_inner(self.context), self.request, contentFilter={'show_inactive': True})
    return table.render()


FolderContentsView.contents_table = contents_table
info('patched %s', str(FolderContentsView.contents_table))