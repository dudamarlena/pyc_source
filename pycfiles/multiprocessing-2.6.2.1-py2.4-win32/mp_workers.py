# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\multiprocessing\examples\mp_workers.py
# Compiled at: 2009-07-30 09:32:52
import time, random
from multiprocessing import Process, Queue, current_process, freeze_support

def worker(input, output):
    for (func, args) in iter(input.get, 'STOP'):
        result = calculate(func, args)
        output.put(result)


def calculate(func, args):
    result = func(*args)
    return '%s says that %s%s = %s' % (current_process().name, func.__name__, args, result)


def mul(a, b):
    time.sleep(0.5 * random.random())
    return a * b


def plus(a, b):
    time.sleep(0.5 * random.random())
    return a + b


def test():
    NUMBER_OF_PROCESSES = 4
    TASKS1 = [ (mul, (i, 7)) for i in range(20) ]
    TASKS2 = [ (plus, (i, 8)) for i in range(10) ]
    task_queue = Queue()
    done_queue = Queue()
    for task in TASKS1:
        task_queue.put(task)

    for i in range(NUMBER_OF_PROCESSES):
        Process(target=worker, args=(task_queue, done_queue)).start()

    print 'Unordered results:'
    for i in range(len(TASKS1)):
        print '\t', done_queue.get()

    for task in TASKS2:
        task_queue.put(task)

    for i in range(len(TASKS2)):
        print '\t', done_queue.get()

    for i in range(NUMBER_OF_PROCESSES):
        task_queue.put('STOP')


if __name__ == '__main__':
    freeze_support()
    test()