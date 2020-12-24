# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/kdb/events.py
# Compiled at: 2014-04-26 09:00:59
"""events

This module defines events shared by various componetns of kdb.
"""
from circuits import Event

class cmd(Event):
    """cmd Event"""
    pass


class reconnect(Event):
    """Rrconnect Event"""
    pass


class terminate(Event):
    """terminate Event"""
    pass