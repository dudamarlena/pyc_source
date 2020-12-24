# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dez/http/wsgithreadpool.py
# Compiled at: 2020-04-19 19:55:58
import threading
try:
    import queue
except:
    import Queue as queue

class WSGIThreadPool(object):

    def __init__(self, num_threads=5):
        self.num_threads = num_threads
        self.work_queue = queue.Queue()
        self.threads = []
        for i in range(self.num_threads):
            self.threads.append(threading.Thread(target=self.run))

    def start(self):
        for i, thread in enumerate(self.threads):
            print (
             'Starting WSGI thread', thread.getName())
            thread.start()

    def dispatch(self, response):
        self.work_queue.put(response)

    def run(self):
        name = threading.currentThread().getName()
        while True:
            try:
                response = self.work_queue.get()
                if not response:
                    break
                response.dispatch()
            except Exception as e:
                import sys, traceback
                print (
                 'error:', e)
                print 'todo: fix exception handling in threads'
                print traceback.print_tb(sys.exc_info()[2])

        print (
         'Shutting down thread', name)

    def stop(self):
        for t in self.threads:
            self.work_queue.put(None)

        return