# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/pycrud/controllers/inbox.py
# Compiled at: 2008-06-20 03:40:59
__doc__ = 'Inbox Controller\n\nAUTHOR: Emanuel Gardaya Calso\n\nLast Modified:\n    2008-03-17\n    2008-03-18\n\n'
import logging
from message import *
log = logging.getLogger(__name__)

class InboxController(MessageController):

    def _init_custom(self):
        c.columns_shown = [
         'sender',
         'message',
         'created']
        c.column_descriptions['created'] = 'Received'

    def _list(self):
        c.entries = self.query.filter_by(folder=1)

    def list(self):
        self._dbg('list')
        c.contacts = get_contacts()
        c.labels = get_labels()
        self._list_params()
        self._list_query()
        self._list()
        return render('/message/inbox_list.mako')

    index = list