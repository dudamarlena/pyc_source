# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/ice/control/controls/details/contents/contents.py
# Compiled at: 2010-08-27 06:32:04
from zope.traversing import api
from zope.app.pagetemplate import ViewPageTemplateFile
from z3c.contents.browser import Contents as ContentsBase
from z3c.contents.column import RenameColumn as RenameColumnBase

class Contents(ContentsBase):
    render = ViewPageTemplateFile('contents.pt')
    allowCopy = False
    allowPaste = False
    batchSize = 10
    startBatchingAt = 10

    def __call__(self):
        self.update()
        return self.render()

    def setupCopyPasteMove(self):
        super(Contents, self).setupCopyPasteMove()
        self.supportsCut = False


class RenameColumn(RenameColumnBase):

    def renderLink(self, item):
        return api.getName(item)