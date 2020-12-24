# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\bzETL\util\multithread.py
# Compiled at: 2013-11-22 17:13:19
import threading
from .struct import nvl
from .logs import Log
from .threads import Queue, Thread
DEBUG = True

class worker_thread(threading.Thread):

    def __init__(self, name, in_queue, out_queue, function):
        threading.Thread.__init__(self)
        self.name = name
        self.in_queue = in_queue
        self.out_queue = out_queue
        self.function = function
        self.keep_running = True
        self.num_runs = 0
        self.start()

    def join(self, timeout=None):
        while self.isAlive():
            Log.note('Waiting on thread {{thread}}', {'thread': self.name})
            threading.Thread.join(self, nvl(timeout, 0.5))

    def run(self):
        got_stop = False
        while self.keep_running:
            request = self.in_queue.pop()
            if request == Thread.STOP:
                got_stop = True
                if self.in_queue.queue:
                    Log.warning('programmer error')
                break
            if not self.keep_running:
                break
            try:
                try:
                    if DEBUG and hasattr(self.function, 'func_name'):
                        Log.note('run {{function}}', {'function': self.function.func_name})
                    result = self.function(**request)
                    if self.out_queue != None:
                        self.out_queue.add({'response': result})
                except Exception as e:
                    Log.warning('Can not execute with params={{params}}', {'params': request}, e)
                    if self.out_queue != None:
                        self.out_queue.add({'exception': e})

            finally:
                self.num_runs += 1

        self.keep_running = False
        if self.num_runs == 0:
            Log.warning('{{name}} thread did no work', {'name': self.name})
        if DEBUG and self.num_runs != 1:
            Log.note('{{name}} thread did {{num}} units of work', {'name': self.name, 
               'num': self.num_runs})
        if got_stop and self.in_queue.queue:
            Log.warning('multithread programmer error')
        if DEBUG:
            Log.note('{{thread}} DONE', {'thread': self.name})
        return

    def stop(self):
        self.keep_running = False


class Multithread(object):

    def __init__(self, functions):
        self.outbound = Queue()
        self.inbound = Queue()
        self.threads = []
        for t, f in enumerate(functions):
            thread = worker_thread('worker ' + unicode(t), self.inbound, self.outbound, f)
            self.threads.append(thread)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        try:
            if isinstance(value, Exception):
                self.inbound.close()
            self.inbound.add(Thread.STOP)
            self.join()
        except Exception as e:
            Log.warning('Problem sending stops', e)

    def join(self):
        try:
            try:
                for t in self.threads:
                    t.join()

            except (KeyboardInterrupt, SystemExit):
                Log.note('Shutdow Started, please be patient')
            except Exception as e:
                Log.error('Unusual shutdown!', e)

        finally:
            for t in self.threads:
                t.keep_running = False

            self.inbound.close()
            self.outbound.close()
            for t in self.threads:
                t.join()

    def execute(self, request):
        self.inbound.extend(request)
        num = len(request)

        def output():
            for i in xrange(num):
                result = self.outbound.pop()
                if 'exception' in result:
                    raise result['exception']
                else:
                    yield result['response']

        return output()

    def stop(self):
        self.inbound.close()
        for t in self.threads:
            t.keep_running = False