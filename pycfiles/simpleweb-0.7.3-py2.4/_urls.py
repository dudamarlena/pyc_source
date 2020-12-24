# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/simpleweb/_urls.py
# Compiled at: 2007-01-10 11:07:05
import dispatcher
__urlmap = dispatcher.Urls()

def urladd(url, controller):
    __urlmap.add(url, controller)


def geturls():
    return __urlmap.geturls()