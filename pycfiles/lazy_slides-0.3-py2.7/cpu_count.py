# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/lazy_slides/cpu_count.py
# Compiled at: 2012-01-02 14:05:57


def cpu_count():
    try:
        import multiprocessing
        return multiprocessing.cpu_count()
    except ImportError:
        raise NotImplementedError()