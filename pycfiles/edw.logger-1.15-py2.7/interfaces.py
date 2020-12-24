# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/edw/logger/events/interfaces.py
# Compiled at: 2018-03-22 05:10:57
from zope.interface import Interface

class IPastedObject(Interface):
    """ Marker interface for objects being pasted. Used in event subscribers.
    """
    pass