# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/sk/seckiss/rfw/rfw/rfwthreads.py
# Compiled at: 2014-03-26 05:27:33
from __future__ import print_function
from threading import Thread
import time, logging, iputil, iptables
from iptables import Iptables
log = logging.getLogger('rfw.rfwthreads')

class CommandProcessor(Thread):

    def __init__(self, cmd_queue, whitelist, expiry_queue, default_expire):
        Thread.__init__(self)
        self.cmd_queue = cmd_queue
        self.whitelist = whitelist
        self.expiry_queue = expiry_queue
        self.default_expire = default_expire
        self.setDaemon(True)

    def schedule_expiry(self, rule, directives):
        expire = directives.get('expire', self.default_expire)
        assert isinstance(expire, str) and expire.isdigit()
        if int(expire):
            expiry_tstamp = time.time() + int(expire)
            extup = (expiry_tstamp, expire, rule)
            self.expiry_queue.put_nowait(extup)
            log.debug(('PUT to Expiry Queue. expiry_queue: {}').format(self.expiry_queue.queue))

    def run(self):
        ruleset = set(Iptables.read_simple_rules())
        while True:
            modify, rule, directives = self.cmd_queue.get()
            try:
                rule_exists = rule in ruleset
                log.debug(('{} rule_exists: {}').format(rule, rule_exists))
                if modify == 'I':
                    if rule_exists:
                        log.warn(('Trying to insert existing rule: {}. Command ignored.').format(rule))
                    else:
                        Iptables.exe_rule(modify, rule)
                        self.schedule_expiry(rule, directives)
                        ruleset.add(rule)
                elif modify == 'D':
                    if rule_exists:
                        Iptables.exe_rule(modify, rule)
                        ruleset.discard(rule)
                    else:
                        log.warn(('Trying to delete not existing rule: {}. Command ignored.').format(rule))
                elif modify == 'L':
                    pass
            finally:
                self.cmd_queue.task_done()


class ExpiryManager(Thread):
    POLL_INTERVAL = 1

    def __init__(self, cmd_queue, expiry_queue):
        """cmd_queue is a FIFO queue of (modify, rcmd) tuples
        expiry_queue is a priority queue of (expiry_tstamp, rcmd) tuples
        """
        Thread.__init__(self)
        self.cmd_queue = cmd_queue
        self.expiry_queue = expiry_queue
        self.setDaemon(True)

    def run(self):

        def peek(q):
            if q.queue:
                return q.queue[0]
            else:
                return
                return

        while True:
            time.sleep(ExpiryManager.POLL_INTERVAL)
            item = peek(self.expiry_queue)
            if item is None:
                continue
            expiry_tstamp, expire, rule = item
            if expiry_tstamp > time.time():
                continue
            try:
                expiry_tstamp, expire, rule = self.expiry_queue.get()
                log.debug(('GET from Expiry Queue. expiry_queue: {}').format(self.expiry_queue.queue))
                directives = {}
                tup = (
                 'D', rule, directives)
                self.cmd_queue.put_nowait(tup)
            finally:
                self.expiry_queue.task_done()

        return


class ServerRunner(Thread):

    def __init__(self, httpd):
        Thread.__init__(self)
        self.httpd = httpd
        self.setDaemon(True)

    def run(self):
        sa = self.httpd.socket.getsockname()
        log.info(('Serving HTTP on {} port {}').format(sa[0], sa[1]))
        self.httpd.serve_forever()