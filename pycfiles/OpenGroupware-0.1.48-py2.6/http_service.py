# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/net/http_service.py
# Compiled at: 2012-10-12 07:02:39
import multiprocessing, os
from time import time
from server import CoilsHTTPServer
from handler import CoilsRequestHandler
from root import RootFolder
from coils.core import *
import logging, logging.config

def serve_forever(server, silent=False):
    try:
        server.run(silent=silent)
    except KeyboardInterrupt:
        pass


class HTTPService(Service):
    __service__ = 'coils.http.manager'
    __auto_dispatch__ = True
    __is_worker__ = True

    def prepare(self):
        self._last_time = time()
        self._workers = {}
        Service.prepare(self)
        RootFolder.load_protocols(self.log)
        sd = ServerDefaultsManager()
        HTTP_HOST = sd.string_for_default('CoilsListenAddress', '127.0.0.1')
        HTTP_PORT = sd.integer_for_default('CoilsListenPort', 8080)
        self.log.info('Starting Server @ %s:%d' % (HTTP_HOST, HTTP_PORT))
        self._httpd = CoilsHTTPServer((HTTP_HOST, HTTP_PORT), CoilsRequestHandler)
        for i in range(15):
            pid = self.start_worker()

        try:
            self.send(Packet('coils.http/__null', 'coils.master/__status', 'HTTP/201 ONLINE'))
        except Exception, e:
            self.log.exception(e)
            sys.exit(1)

    def start_worker(self):
        p = multiprocessing.Process(target=serve_forever, args=(
         self._httpd,))
        p.start()
        self._workers[p.pid] = p
        self.log.info(('Started HTTP worker PID#{0}').format(p.pid))
        return p.pid

    def work(self):
        if time() - self._last_time > 15:
            self._last_time = time()
            drop = []
            for pid in self._workers:
                worker = self._workers[pid]
                worker.join(0.1)
                if worker.is_alive():
                    pass
                else:
                    self.log.debug(('HTTP workerId#{0} has failed').format(pid))
                    drop.append(pid)

            if len(drop) > 0:
                for pid in drop:
                    del self._workers[pid]
                    new_pid = self.start_worker()
                    message = ('HTTP workerId#{0} has failed, new workerId#{1} has been created.').format(pid, new_pid)
                    self.log.info(message)