# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.darwin-9.6.0-i386/egg/astrogrid/threadpool.py
# Compiled at: 2007-06-17 06:12:42
import threading, Queue, time, sys, traceback

class easy_pool:
    __module__ = __name__

    def __init__(self, func):
        self.Qin = Queue.Queue()
        self.Qout = Queue.Queue()
        self.Qerr = Queue.Queue()
        self.Pool = []
        self.Func = func

    def process_queue(self):
        flag = 'ok'
        while flag != 'stop':
            (flag, item) = self.Qin.get()
            if flag == 'ok':
                try:
                    self.Qout.put(self.Func(*item))
                except:
                    self.Qerr.put(self.err_msg())

    def start_threads(self, num_threads=5):
        for i in range(num_threads):
            thread = threading.Thread(target=self.process_queue)
            thread.start()
            self.Pool.append(thread)

    def put(self, data, flag='ok'):
        self.Qin.put([flag, data])

    def get(self):
        return self.Qout.get()

    def get_errors(self):
        try:
            while 1:
                yield self.Qerr.get_nowait()

        except Queue.Empty:
            pass

    def get_all(self):
        try:
            while 1:
                yield self.Qout.get_nowait()

        except Queue.Empty:
            pass

    def stop_threads(self):
        for i in range(len(self.Pool)):
            self.Qin.put(('stop', None))

        while self.Pool:
            time.sleep(0.1)
            for (index, the_thread) in enumerate(self.Pool):
                if the_thread.isAlive():
                    continue
                else:
                    del self.Pool[index]
                break

        return

    def run_all(self, asap=None, num_threads=10):
        if asap:
            self.start_threads(num_threads)
            yield self.get()
            while self.Qin.qsize():
                for i in self.get_all():
                    yield i
                    time.sleep(60)

            self.stop_threads()
            for i in self.get_all():
                yield i

        self.start_threads(num_threads)
        self.stop_threads()
        for i in self.get_all():
            yield i

    def err_msg(self):
        trace = sys.exc_info()[2]
        try:
            exc_value = str(sys.exc_value)
        except:
            exc_value = ''

        return (
         str(traceback.format_tb(trace)), str(sys.exc_type), exc_value)

    def qinfo(self):
        return ('in', self.Qin.qsize(), 'out', self.Qout.qsize())