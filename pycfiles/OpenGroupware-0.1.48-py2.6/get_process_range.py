# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/workflow/get_process_range.py
# Compiled at: 2012-10-12 07:02:39
from datetime import datetime, timedelta
from sqlalchemy import *
from coils.foundation import *
from coils.core import *
from coils.core.logic import GetCommand

class GetProcessRange(GetCommand):
    __domain__ = 'process'
    __operation__ = 'get-range'

    def __init__(self):
        GetCommand.__init__(self)

    def prepare(self, ctx, **params):
        self.start = datetime.today()
        self.span = timedelta(days=8)
        self.end = self.start + self.span
        self.set_multiple_result_mode()
        GetCommand.prepare(self, ctx, **params)

    def parse_parameters(self, **params):
        Command.parse_parameters(self, **params)
        self.parse_range(start=params.get('start', None), end=params.get('end', None), span=params.get('span', None))
        return

    def parse_range(self, start=None, end=None, span=None):
        if start is None:
            self.start = self._ctx.get_utctime() - timedelta(days=1)
        else:
            self.start = start
        if span is None:
            self.span = timedelta(days=45)
        else:
            self.span = timedelta(days=int(span))
            self.end = self.start + self.span
        if end is None:
            self.end = self.start + self.span
        else:
            self.end = end
        return

    def get_query(self):
        db = self._ctx.db_session()
        query = db.query(Process)
        query = query.filter(Process.created > self.start)
        query = query.filter(Process.created < self.end)
        return query

    def run(self):
        query = self.get_query()
        self.set_return_value(query.all())