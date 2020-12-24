# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ice/template/browser/storages.py
# Compiled at: 2009-05-04 14:30:04
from z3c.table import table, column
from zope.component import getAllUtilitiesRegisteredFor
from zope.dublincore.interfaces import IZopeDublinCore
from ice.template.interfaces import ITemplates
from ice.template import _

class Pagelet(table.Table):
    __module__ = __name__

    @property
    def values(self):
        return getAllUtilitiesRegisteredFor(ITemplates, self.context)


class TitleLinkColumn(column.IndexLinkColumn):
    __module__ = __name__
    header = _('Name')

    def getLinkContent(self, item):
        return IZopeDublinCore(item).title or super(TitleLinkColumn, self).getLinkContent(item)