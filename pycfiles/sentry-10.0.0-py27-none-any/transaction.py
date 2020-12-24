# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/eventtypes/transaction.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
from sentry.utils.safe import get_path
from .base import BaseEvent

class TransactionEvent(BaseEvent):
    key = 'transaction'

    def get_metadata(self, data):
        description = get_path(data, 'contexts', 'trace', 'description')
        transaction = get_path(data, 'transaction')
        return {'title': description or transaction, 'location': transaction}

    def get_title(self, metadata):
        return metadata['title']

    def get_location(self, metadata):
        return metadata['location']