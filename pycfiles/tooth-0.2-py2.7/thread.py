# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tooth/thread.py
# Compiled at: 2015-04-29 20:46:50
__author__ = 'Tom James Holub'
import threading

def delegate(callback, args_list=None, args_dict=None):
    delegator = FunctionDelegator(callback, args_list or [], args_dict or {})
    delegator.start()


class FunctionDelegator(threading.Thread):

    def __init__(self, callback, args_list, args_dict):
        threading.Thread.__init__(self)
        self.cb = callback
        self.list = args_list
        self.dict = args_dict

    def run(self):
        self.cb(*self.list, **self.dict)