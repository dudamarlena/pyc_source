# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/uittenbroek/Projects/buildout-nuffic/src/collective.newrelic/collective/newrelic/patches/newrelic_transaction.py
# Compiled at: 2013-12-24 05:41:42
from collective.newrelic.utils import logger
from newrelic.api.transaction import Transaction
original__init__ = Transaction.__init__
original__exit__ = Transaction.__exit__

def patched__init__(self, *args, **kwargs):
    original__init__(self, *args, **kwargs)
    self._transaction_id = id(self)


Transaction.__init__ = patched__init__
logger.info('Patched newrelic.api.transaction:Transaction.__init__ to add _transaction_id')

def patched__exit__(self, *args, **kwargs):
    if self._transaction_id != id(self):
        logger.exception(('Checking my id: {0}  against {1}').format(self._transaction_id, id(self)))
        return
    original__exit__(self, *args, **kwargs)


Transaction.__exit__ = patched__exit__
logger.info('Patched newrelic.api.transaction:Transaction.__exit__ to check _transaction_id')