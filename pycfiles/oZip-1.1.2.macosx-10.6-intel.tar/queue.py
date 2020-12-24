# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/oZip/queue.py
# Compiled at: 2014-08-30 09:16:39
from Queue import Queue
from threading import Thread
import time
from main import main

def Worker(i, q, err_q, decompress):
    """ A Worker thread to process a file """
    while True:
        filename = q.get()
        res = main(filename, decompress)
        if isinstance(res, tuple):
            err_q.put(res)
        q.task_done()


def runPool(f_list, err_q, should_compress=False, pool_size=5):
    """ Create a thread pool to process a queue of files """
    if len(f_list) < pool_size:
        pool_size = len(f_list)
    files_queue = Queue()
    for i in range(pool_size):
        worker = Thread(target=Worker, args=(i, files_queue, err_q, should_compress))
        worker.setDaemon(True)
        worker.start()

    for filename in f_list:
        files_queue.put(filename)

    files_queue.join()
    err_q.join()
    err_q.put('Done')