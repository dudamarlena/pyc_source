# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site-packages/mailhandler/core.py
# Compiled at: 2019-09-10 05:47:40
# Size of source mod 2**32: 615 bytes
from mailhandler.tracking.adapters import TrackingAdapter
from mailhandler.transactional.adapters import TransactionalAdapter
from mailhandler.bulk.adapters import BulkAdapter

class Client:
    token = None
    adapters = (
     TrackingAdapter,
     TransactionalAdapter,
     BulkAdapter)

    def __init__(self, token):
        self.token = token
        self.setup_adapters()

    def setup_adapters(self):
        for adapter_class in self.adapters:
            instance = adapter_class(headers={'X-Secure-Token': self.token})
            setattr(self, instance.name, instance)