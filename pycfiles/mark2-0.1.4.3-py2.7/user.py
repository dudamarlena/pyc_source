# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mk2/events/user.py
# Compiled at: 2013-08-16 22:15:55
from . import Event

class UserInput(Event):
    user = Event.Arg(required=True)
    line = Event.Arg(required=True)


class UserAttach(Event):
    user = Event.Arg(required=True)


class UserDetach(Event):
    user = Event.Arg(required=True)