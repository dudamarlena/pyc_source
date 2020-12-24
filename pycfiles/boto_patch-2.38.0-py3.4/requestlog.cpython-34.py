# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/boto/requestlog.py
# Compiled at: 2015-11-24 05:02:18
# Size of source mod 2**32: 1486 bytes
import sys
from datetime import datetime
from threading import Thread
import Queue
from boto.utils import RequestHook
from boto.compat import long_type

class RequestLogger(RequestHook):
    __doc__ = '\n    This class implements a request logger that uses a single thread to\n    write to a log file.\n    '

    def __init__(self, filename='/tmp/request_log.csv'):
        self.request_log_file = open(filename, 'w')
        self.request_log_queue = Queue.Queue(100)
        Thread(target=self._request_log_worker).start()

    def handle_request_data(self, request, response, error=False):
        len = 0 if error else response.getheader('Content-Length')
        now = datetime.now()
        time = now.strftime('%Y-%m-%d %H:%M:%S')
        td = now - request.start_time
        duration = (td.microseconds + long_type(td.seconds + td.days * 24 * 3600) * 1000000.0) / 1000000.0
        self.request_log_queue.put("'%s', '%s', '%s', '%s', '%s'\n" % (time, response.status, duration, len, request.params['Action']))

    def _request_log_worker(self):
        while True:
            try:
                item = self.request_log_queue.get(True)
                self.request_log_file.write(item)
                self.request_log_file.flush()
                self.request_log_queue.task_done()
            except:
                import traceback
                traceback.print_exc(file=sys.stdout)