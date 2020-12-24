# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/charles/code/huey/examples/simple/tasks.py
# Compiled at: 2019-03-18 22:39:39
# Size of source mod 2**32: 1084 bytes
import time
from huey import crontab
from config import huey

def tprint(s, c=32):
    print('\x1b[1;%sm%s\x1b[0m' % (c, s))


@huey.task()
def add(a, b):
    return a + b


@huey.task()
def mul(a, b):
    return a * b


@huey.task()
def slow(n):
    tprint('going to sleep for %s seconds' % n)
    time.sleep(n)
    tprint('finished sleeping for %s seconds' % n)
    return n


@huey.task(retries=1, retry_delay=5, context=True)
def flaky_task(task=None):
    if task is not None:
        if task.retries == 0:
            tprint('flaky task succeeded on retry.')
            return 'succeeded on retry.'
    tprint('flaky task is about to raise an exception.', 31)
    raise Exception('flaky task failed!')


@huey.periodic_task(crontab(minute='*/2'))
def every_other_minute():
    tprint('This task runs every 2 minutes.', 35)


@huey.periodic_task(crontab(minute='*/5'))
def every_five_mins():
    tprint('This task runs every 5 minutes.', 34)