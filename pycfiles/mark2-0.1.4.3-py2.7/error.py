# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mk2/events/error.py
# Compiled at: 2013-08-16 22:15:55
from . import Event

class Error(Event):
    pass


class FatalError(Event):
    exception = Event.Arg()
    reason = Event.Arg()