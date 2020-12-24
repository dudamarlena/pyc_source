# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/net/server.py
# Compiled at: 2012-10-12 07:02:39
import time, logging, pprint, traceback
from coils.core import *
import BaseHTTPServer, socket, os, resource, gc
from coils.foundation.api import objgraph as COILS_objgraph

class CoilsHTTPServer(Service, BaseHTTPServer.HTTPServer):
    __HTTPRSSDebugOn__ = None
    __HTTPRSSLimit__ = None
    __HTTPReqLimit__ = None
    __service__ = 'coils.http.$$'

    def __init__(self, listen, handler):
        BaseHTTPServer.HTTPServer.__init__(self, listen, handler)
        self._shutdown = False
        if CoilsHTTPServer.__HTTPRSSDebugOn__ is None:
            CoilsHTTPServer.__HTTPRSSDebugOn__ = ServerDefaultsManager().bool_for_default('HTTPMemoryDebugEnabled')
        if CoilsHTTPServer.__HTTPRSSLimit__ is None:
            CoilsHTTPServer.__HTTPRSSLimit__ = ServerDefaultsManager().integer_for_default('HTTPWorkerMemoryLimit', 128000000)
        if CoilsHTTPServer.__HTTPReqLimit__ is None:
            CoilsHTTPServer.__HTTPReqLimit__ = ServerDefaultsManager().integer_for_default('HTTPWorkerRequestLimit', 256)
        return

    @property
    def rss_debug_enabled(self):
        return CoilsHTTPServer.__HTTPRSSDebugOn__

    @property
    def broker(self):
        return self._broker

    def server_bind(self):
        BaseHTTPServer.HTTPServer.server_bind(self)

    def receive_message(self, message):
        pass

    def prepare(self):
        Service.prepare(self)
        self._previous_rss = 0
        self._check_rss = False
        self.socket.settimeout(10)
        if CoilsHTTPServer.__HTTPRSSDebugOn__:
            self.log.debug('RSS Debugging is enabled')
        else:
            self.log.debug('RSS Debugging is disabled')
        self.log.info(('RSS limit is {0}').format(CoilsHTTPServer.__HTTPRSSLimit__))
        self.log.info(('Request limit is {0}').format(CoilsHTTPServer.__HTTPReqLimit__))

    def receive_message(self, message):
        Service.receive_message(self, message)

    def check_messages(self):
        self.wait(timeout=0.1)

    def get_rss_size(self):
        rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * 1000
        if rss == 0:
            try:
                handle = open(('/proc/{0}/statm').format(os.getpid()), 'rb')
                data = handle.read(512)
                handle.close()
                rss = int(data.split(' ')[1]) * 4000
            except Exception, e:
                rss = 0

        return rss

    def rss_check(self):
        collected = gc.collect()
        rss = self.get_rss_size()
        rss_difference = rss - self._previous_rss
        self._previous_rss = rss
        if rss > 0:
            if rss > CoilsHTTPServer.__HTTPRSSLimit__:
                self._shutdown = True
                self.check_messages()
                self.log.info('HTTP worker has exceeded maximum RSS size, shutting down.')
        if self.rss_debug_enabled:
            self.log.info(('RSS is {0} (delta={1})').format(rss, rss_difference))
            payload = COILS_objgraph.get_most_common_types(limit=25)
            try:
                if rss_difference > 128:
                    message = ('RSS Change of {0} for {1}.\n\n').format(rss_difference, self.__service__)
                    message = ('{0} objects garbage collected before RSS check.\n').format(collected)
                    message = ('{0}{1}').format(message, pprint.pformat(payload))
                    self.send_administrative_notice(category='network', urgency=1, subject=('HTTP workerId#{0} object allocation report.').format(os.getpid()), message=message)
            except Exception, e:
                self.log.exception(e)

    def request_count_check(self):
        if CoilsHTTPServer.__HTTPReqLimit__ < self.request_count:
            self._shutdown = True

    def get_request(self):
        self.socket.settimeout(10)
        try:
            if self._check_rss:
                self.rss_check()
        except Exception, e:
            self.log.error('Exception performing worker RSS check')
            self.log.exception(e)
            self.send_administrative_notice(category='network', urgency=8, subject=('Exception performing RSS check for workerId#{0}').format(os.getpid()), message=('Worker is requesting shutdown.\n\n{0}').format(traceback.format_exc()))

        try:
            self.request_count_check()
        except Exception, e:
            self.log.error('Exception performing worker request count check')
            self.log.exception(e)
            self.send_administrative_notice(category='network', urgency=8, subject=('Exception checking request count for workerId#{0}').format(os.getpid()), message=('Worker is requesting shutdown.\n\n{0}').format(traceback.format_exc()))

        while not self._shutdown:
            self.check_messages()
            try:
                self._check_rss = False
                (s, a) = self.socket.accept()
                s.settimeout(None)
                self._check_rss = True
                self.log.debug('Incremented request count')
                self.request_count += 1
                return (s, a)
            except socket.timeout:
                pass
            except socket.error, e:
                time.sleep(0.1)
            except Exception, e:
                self.log.exception(e)
                self.send_administrative_notice(category='network', urgency=8, subject=('Unrecoverable exception in HTTP workerId#{0}').format(os.getpid()), message=('Worker is requesting shutdown.\n\n{0}').format(traceback.format_exc()))
                self._shutdown = True

        return (None, None)

    def run(self, silent=True):
        self.request_count = 0
        self.setup(silent=silent)
        self.prepare()
        self.serve_forever()