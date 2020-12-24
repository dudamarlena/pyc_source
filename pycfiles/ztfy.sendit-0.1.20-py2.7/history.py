# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/sendit/skin/app/history.py
# Compiled at: 2014-05-12 04:44:17
__docformat__ = 'restructuredtext'
from z3c.table.interfaces import IBatchProvider
from ztfy.sendit.app.interfaces import ISenditApplication
from ztfy.sendit.profile.interfaces.history import IProfileHistory
from ztfy.sendit.skin.layer import ISenditLayer
from z3c.table.batch import BatchProvider
from z3c.table.column import GetAttrColumn, Column
from z3c.table.table import Table
from zope.browserpage.viewpagetemplatefile import ViewPageTemplateFile
from zope.component import adapts
from zope.interface import implements
from ztfy.sendit.skin.page import BaseSenditApplicationPage
from ztfy.utils.date import formatDatetime, formatDate
from ztfy.utils.size import getHumanSize
from ztfy.sendit import _

class SenditApplicationHistory(BaseSenditApplicationPage, Table):
    """Sendit application history view"""
    shortname = _('History')
    cssClasses = {'table': 'table table-bordered table-striped table-hover'}
    sortOn = None
    batchSize = 20
    startBatchingAt = 20

    def __init__(self, context, request):
        BaseSenditApplicationPage.__init__(self, context, request)
        Table.__init__(self, context, request)

    def update(self):
        BaseSenditApplicationPage.update(self)
        Table.update(self)

    @property
    def values(self):
        history = IProfileHistory(self.request.principal)
        return sorted(history.values(), key=lambda x: x.creation_time, reverse=True)


class SendedColumn(GetAttrColumn):
    """History sended date column"""
    header = _('Send on')
    cssClasses = {'th': 'span3', 'td': 'small'}
    weight = 0

    def getValue(self, obj):
        return formatDatetime(obj.creation_time, request=self.request)


class PacketColumn(Column):
    """Outbox packet column"""
    header = _('Packet content')
    template = ViewPageTemplateFile('templates/history_packet.pt')
    weight = 10

    def renderCell(self, item):
        self.context = item
        return self.template(self)

    def getSize(self, document):
        return getHumanSize(document.contentSize)

    def getDate(self, date):
        return formatDatetime(date, request=self.request)

    def getExpirationDate(self):
        return formatDate(self.context.expiration_date, request=self.request)

    def getArchiveDate(self):
        return formatDatetime(self.context.deletion_time, request=self.request)


class SenditApplicationHistoryBatchProvider(BatchProvider):
    """History batch provider"""
    adapts(ISenditApplication, ISenditLayer, SenditApplicationHistory)
    implements(IBatchProvider)

    def renderBatchLink(self, batch, cssClass=None):
        return '<li%s>%s</li>' % (' class="active"' if batch == self.batch else '',
         super(SenditApplicationHistoryBatchProvider, self).renderBatchLink(batch, cssClass))