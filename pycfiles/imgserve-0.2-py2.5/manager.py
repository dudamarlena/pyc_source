# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/imgserve/manager.py
# Compiled at: 2009-08-22 09:02:52
"""
Manages the http server process and worker processes and communication
among them.
"""
import sys, time, os, signal, Queue
from multiprocessing import Process, cpu_count, JoinableQueue
from imgserve.http import httpserv
from imgserve.worker import work

class ImgManager:
    """
    This manager starts the http server processes and worker
    processes, creates the input/output queues that keep the processes
    work together nicely.
    """

    def __init__(self):
        self.NUMBER_OF_PROCESSES = cpu_count()

    def start(self, host, port):
        self.i_queue = JoinableQueue()
        self.o_queue = JoinableQueue()
        print 'Starting %s worker process(es)' % self.NUMBER_OF_PROCESSES
        self.workers = [ Process(target=work, name='imgserve: worker process %s' % str(i + 1), args=(self.i_queue, self.o_queue)) for i in range(self.NUMBER_OF_PROCESSES)
                       ]
        for w in self.workers:
            w.start()
            print 'Worker process ' + str(w.pid) + ' started'

        self.http = Process(target=httpserv, args=(host, port,
         self.i_queue, self.o_queue))
        self.name = 'imgserve: http server'
        self.http.start()
        print 'HTTP process ' + str(self.http.pid) + ' started'
        self.running = True
        while self.running:
            time.sleep(1)

        self.http.join()

    def stop(self):
        print 'imgserve shutting down'
        os.kill(self.http.pid, signal.SIGINT)
        while True:
            try:
                self.o_queue.task_done()
            except ValueError:
                break

        self.o_queue.join()
        self.i_queue.put(None)
        for w in self.workers:
            w.join()

        assert self.i_queue.get() is None
        assert self.i_queue.qsize() is 0
        while True:
            try:
                self.i_queue.task_done()
            except ValueError:
                break

        self.i_queue.join()
        self.running = False
        return

    def kill(self):
        """Stop violently."""
        self.http.terminate()
        for w in self.workers:
            w.terminate()
            print 'Terminate worker process'

        self.running = False
        print 'Change self.running to False'