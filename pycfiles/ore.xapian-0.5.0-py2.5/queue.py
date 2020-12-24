# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/ore/xapian/queue.py
# Compiled at: 2008-10-15 08:53:48
"""
$Id: $
"""
import Queue, threading, time
from logging import getLogger
from ore.xapian import interfaces
index_queue = Queue.Queue()
log = getLogger('ore.xapian')

class QueueProcessor(object):
    FLUSH_THRESHOLD = 20
    POLL_TIMEOUT = 60
    indexer_running = False
    indexer_thread = None

    def __init__(self, connection):
        self.connection = connection

    def operations(self):
        while self.indexer_running:
            try:
                op = index_queue.get(True, self.POLL_TIMEOUT)
            except Queue.Empty:
                yield
            else:
                yield op

        return

    def __call__(self):
        op_delta = 0
        for op in self.operations():
            if op is None:
                if op_delta:
                    if interfaces.DEBUG_LOG:
                        log.info('QueueProcessor:Timeout Flushing Index %s Pending Ops' % op_delta)
                    self.connection.flush()
                    op_delta = 0
                continue
            if interfaces.DEBUG_LOG:
                log.debug('Processing Operation %r %r' % (op.document_id, op))
            try:
                result = op.process(self.connection)
            except:
                log.exception('Error During Operation %r %r' % (op.document_id, op))
                continue

            op_delta += 1
            if op_delta % self.FLUSH_THRESHOLD == 0:
                if interfaces.DEBUG_LOG:
                    log.info('QueueProcessor:Delta Flushing Index %s Pending Ops' % op_delta)
                self.connection.flush()
                op_delta = 0

        return

    @classmethod
    def start(klass, connection, silent=False):
        if klass.indexer_running:
            if silent:
                return
            raise SyntaxError('Indexer already running')
        if interfaces.DEBUG_LOG:
            log.info('Starting QueueProcessor Thread')
            log.debug('Index Fields Defined')
        klass.indexer_running = True
        indexer = klass(connection)
        klass.indexer_thread = threading.Thread(target=indexer)
        klass.indexer_thread.setDaemon(True)
        klass.indexer_thread.start()
        return indexer

    @classmethod
    def stop(klass):
        if not klass.indexer_running:
            return
        if interfaces.DEBUG_LOG:
            log.info('Stopping QueueProcessor Thread')
        klass.indexer_running = False
        klass.indexer_thread.join()
        if interfaces.DEBUG_LOG:
            log.info('Stopped QueueProcessor Thread')