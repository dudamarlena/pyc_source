# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/vagoth/transaction.py
# Compiled at: 2013-02-24 05:07:26
"""
Wrap any code block in a transaction in order to get
a transaction id in the logs.

Example:

>>> with Transaction(username):
...    manager.action("start", vm_name="my_vm")

Nested transaction's will retain the first transaction ID, instead of generating a
new one.
"""
import threading, uuid
threadlocal = threading.local()
threadlocal.vagoth_txid = None
threadlocal.source = None

def get_txid():
    """
    Return the current transaction ID, or "0"
    """
    global threadlocal
    try:
        return threadlocal.vagoth_txid or '0'
    except AttributeError:
        return '0'


def get_source():
    """
    Return the current transaction source, or "0"
    """
    try:
        return threadlocal.source or '0'
    except AttributeError:
        return '0'


class Transaction(object):
    """
    Transaction(source=None, txid=None)

    source might be a username, or the name of the process.

    If a transaction is already set for the current thread, it
    will be used instead of the passed-in txid.

    If txid is not specified, a random one will be generated.
    """

    def __init__(self, source=None, txid=None):
        self.source = source
        self.desired_txid = txid

    def __enter__(self):
        self.txid = None
        if threadlocal.vagoth_txid == None:
            self.txid = self.desired_txid or uuid.uuid4().hex[:8]
            threadlocal.vagoth_txid = self.txid
            threadlocal.source = self.source
        return

    def __exit__(self, *args, **kwargs):
        if self.txid != None:
            threadlocal.vagoth_txid = None
            threadlocal.source = None
        return