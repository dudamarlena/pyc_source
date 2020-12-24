# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\aigpy\threadHelper.py
# Compiled at: 2019-10-26 00:11:28
# Size of source mod 2**32: 2366 bytes
"""
@File    :   threadHelper.py
@Time    :   2018/12/17
@Author  :   Yaron Huang 
@Version :   1.0
@Contact :   yaronhuang@qq.com
@Desc    :   Thread Tool 
"""
import sys, threading
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed
from concurrent.futures import wait
from concurrent.futures import ALL_COMPLETED

class ThreadTool(object):

    def __init__(self, maxThreadNum):
        self.allTask = []
        self.thread = ThreadPoolExecutor(max_workers=maxThreadNum)

    def start(self, function, *args, **kwargs):
        if len(args) > 0 and len(kwargs) > 0:
            handle = (self.thread.submit)(function, *args, **kwargs)
        else:
            if len(args) > 0:
                handle = (self.thread.submit)(function, *args)
            else:
                if len(kwargs) > 0:
                    handle = (self.thread.submit)(function, **kwargs)
                else:
                    handle = self.thread.submit(function)
        self.allTask.append(handle)
        return handle

    def isFinish(self, handle):
        return handle.done()

    def getResult(self, handle):
        return handle.result()

    def waitAll(self):
        for future in as_completed(self.allTask):
            data = future.result()

    def waitAnyone(self):
        as_completed(self.allTask)

    def close(self):
        self.thread.shutdown(False)


class ThreadPoolManger(object):

    def __init__(self, maxThreadNum):
        v = sys.version_info
        if v[0] > 2:
            import queue
            self.work_queue = queue.Queue()
        else:
            import Queue
            self.work_queue = Queue.Queue()
        self.allTask = []
        self.thread = ThreadPoolExecutor(max_workers=maxThreadNum)
        for i in range(maxThreadNum):
            handle = self.thread.submit(self.__workThread__)
            self.allTask.append(handle)

    def __workThread__(self):
        while True:
            func, args = self.work_queue.get()
            func(*args)
            self.work_queue.task_done()

    def addWork(self, func, *args):
        self.work_queue.put((func, args))

    def close(self):
        self.thread.shutdown(False)