# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/pycrud/controllers/sent.py
# Compiled at: 2008-06-20 03:40:59
import logging
from message import *
log = logging.getLogger(__name__)

class SentController(MessageController):

    def _init_custom(self):
        c.columns_shown = [
         'recipient',
         'message',
         'created']
        c.column_descriptions['created'] = 'Sent'

    def _list(self):
        c.entries = self.query.filter_by(folder=4)