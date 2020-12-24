# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/breezekay/Dropbox/Codes/ez/py.ez.co/comb.ez.co/comb/combd.py
# Compiled at: 2014-11-28 04:05:13
# Size of source mod 2**32: 2388 bytes
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
    print('\nUser interrupt.Waiting Threads exist.\n')
    if '--debug' in sys.argv:
        sys.exit(-1)


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
                    print('User interrupt on thread:', threading.current_thread())
                    sys.exit(0)


class Start(object):

    def __init__(self, slot, extra_loader={}, debug=False, thread_nums=10, sleep_cycle=2, sleep_max=60, once=False, no_daemon=False, *args, **kwargs):
        self.debug = debug
        self.threads_num = thread_nums
        self.sleep_max = sleep_max
        self.sleep = sleep_cycle
        self.extra_loader = extra_loader
        self.once = once
        self.no_daemon = no_daemon
        if slot:
            iterator = slot(self)
            threads_num = iterator.threads_num
            i = 0
            while i < threads_num:
                t = Thread(target=worker, args=[iterator])
                if self.once is False:
                    if self.no_daemon:
                        t.daemon = False
                    else:
                        t.daemon = True
                t.start()
                i += 1

            if self.once is False:
                while True:
                    if threading.active_count() > 1:
                        sleep(1)
                    elif threading.current_thread().name == 'MainThread':
                        sys.exit(0)
                        continue