# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nodeconductor_killbill/log.py
# Compiled at: 2016-09-25 09:47:37
from nodeconductor.logging.loggers import EventLogger, event_logger
from .models import Invoice

class InvoiceEventLogger(EventLogger):
    invoice = Invoice

    class Meta:
        event_types = ('invoice_deletion_succeeded', 'invoice_update_succeeded', 'invoice_creation_succeeded')


event_logger.register('killbill_invoice', InvoiceEventLogger)