# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pycrud/controllers/inbox.py
# Compiled at: 2008-06-20 03:40:59
"""Inbox Controller

AUTHOR: Emanuel Gardaya Calso

Last Modified:
    2008-03-17
    2008-03-18

"""
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