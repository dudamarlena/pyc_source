# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\stacklesslib\replacements\select.py
# Compiled at: 2017-12-11 20:12:50
from __future__ import absolute_import
import stackless, stacklesslib.threadpool, select as real_select
error = real_select.error
__doc__ = real_select.__doc__
_main_thread_id = stackless.main.thread_id

def select(*args, **kwargs):
    if stackless.current.thread_id == _main_thread_id:
        if len(args) == 3 or len(args) == 4 and (args[3] is None or args[3] > 0.05) or 'timeout' in kwargs and (kwargs['timeout'] is None or kwargs['timeout'] > 0.05):
            return stacklesslib.threadpool.call_on_thread(real_select.select, args, kwargs)
    return real_select.select(*args)


select.__doc__ = real_select.select.__doc__