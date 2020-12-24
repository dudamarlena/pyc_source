# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/breezekay/Dropbox/Codes/ez/py.ez.co/comb.ez.co/comb/combd.py
# Compiled at: 2014-11-06 09:34:33
import os, sys, signal
from threading import Thread
from time import sleep
import threading
_exist_flag = False

def get_exist_flag():
    global _exist_flag
    return _exist_flag


def set_exist_flag(flag):
    global _exist_flag
    _exist_flag = flag


def signal_handle(signum, frame):
    set_exist_flag(True)
    print '\nUser interrupt.Waiting Threads exist.\n'
    print sys.argv


signal.signal(signal.SIGINT, signal_handle)

def worker(iterator):
    time = iterator.sleep
    while True:
        with iterator as (result):
            if result is not False:
                iterator.slot(result)
                time = iterator.sleep
            else:
                if iterator.combd.once is True:
                    sys.exit(0)
                if get_exist_flag() is False:
                    time += iterator.sleep
                    if time > iterator.sleep_max:
                        time = iterator.sleep
                    sleep(time)
                else:
                    print (
                     'User interrupt on thread:', threading.current_thread())
                    sys.exit(0)


class Start(object):

    def __init__(self, slot, extra_loader={}, debug=False, thread_nums=10, sleep_cycle=2, sleep_max=60, once=False, *args, **kwargs):
        self.debug = debug
        self.threads_num = thread_nums
        self.sleep_max = sleep_max
        self.sleep = sleep_cycle
        self.extra_loader = extra_loader
        self.once = once
        if slot:
            iterator = slot(self)
            threads_num = iterator.threads_num
            i = 0
            while i < threads_num:
                t = Thread(target=worker, args=[iterator])
                if self.once is False:
                    t.daemon = True
                t.start()
                i += 1

            if self.once is False:
                while True:
                    if threading.active_count() > 1:
                        sleep(1)
                    elif threading.current_thread().name == 'MainThread':
                        sys.exit(0)