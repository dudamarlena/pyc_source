# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/ycyc/frameworks/spider/utils.py
# Compiled at: 2016-02-25 04:17:16


def save_to(path, data, mode='ab'):
    with open(path, mode) as (fp):
        fp.write(data)


def flow_return():
    raise StopIteration