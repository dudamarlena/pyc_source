# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\bzETL\util\multiprocess.py
# Compiled at: 2013-11-22 17:13:19
from multiprocessing.queues import Queue
from .logs import Log

class worker(object):

    def __init__(func, inbound, outbound, logging):
        logger = Log_usingInterProcessQueue(logging)


class Log_usingInterProcessQueue(Log):

    def __init__(self, outbound):
        self.outbound = outbound

    def write(self, template, params):
        self.outbound.put({'template': template, 'param': params})


class Multiprocess(object):

    def __init__(self, functions):
        self.outbound = Queue()
        self.inbound = Queue()
        self.inbound = Queue()
        self.threads = []
        for t, f in enumerate(functions):
            thread = worker('worker ' + unicode(t), f, self.inbound, self.outbound)
            self.threads.append(thread)

    def __enter__(self):
        return self

    def __exit__(self, a, b, c):
        try:
            self.inbound.close()
        except Exception as e:
            Log.warning('Problem adding to inbound', e)

        self.join()

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

            for t in self.threads:
                t.join()

            self.inbound.close()
            self.outbound.close()

    def execute(self, parameters):
        self.inbound.extend(parameters)
        num = len(parameters)

        def output():
            for i in xrange(num):
                result = self.outbound.pop()
                yield result

        return output()

    def stop(self):
        self.inbound.close()
        for t in self.threads:
            t.keep_running = False