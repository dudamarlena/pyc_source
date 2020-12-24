# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/zwsun/workspace/python/corunner/corunner/common/SimpleThreadPool.py
# Compiled at: 2013-11-05 08:22:06
import threading, Queue

class Task:

    def run(self):
        pass


class Worker(threading.Thread):

    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue
        self.end = False

    def run(self):
        while True:
            task = None
            try:
                task = self.queue.get(True, 1)
            except:
                pass

            if task is not None:
                try:
                    task.run()
                finally:
                    self.queue.task_done()

            if self.end:
                break

        return


class SimpleThreadPool:

    def __init__(self, nWorker, nQueue=0):
        self.nWorker = nWorker
        self.nQueue = nQueue
        self.queue = Queue.Queue(nQueue)
        self.workers = []
        for i in range(nWorker):
            self.workers.append(self.__newWorker())

    def __newWorker(self):
        worker = Worker(self.queue)
        worker.setName('pool-worker-' + str(len(self.workers)))
        worker.setDaemon(True)
        worker.start()
        return worker

    def addTask(self, task, block=True, timeout=None):
        self.queue.put(task, block, timeout)

    def await(self):
        self.queue.join()

    def close(self):
        self.await()
        for w in self.workers:
            w.end = True