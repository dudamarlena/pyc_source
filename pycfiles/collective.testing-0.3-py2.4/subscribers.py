# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.darwin-8.9.1-i386/egg/collective/testing/subscribers.py
# Compiled at: 2007-04-17 11:47:01
from cStringIO import StringIO
from zope.interface import Interface

class EventPrinter(object):
    __module__ = __name__
    _event_filter = Interface
    _interface = Interface

    def __init__(self, buffer):
        self.buffer = buffer

    def channelPrinter(self, obj, event):
        if self._interface.providedBy(obj) or self._event_filter.providedBy(event):
            print >> self.buffer, '%s.%s :: %s %s' % (event.__module__, event.__class__.__name__, obj, obj.getId())

    def eventPrinter(self, event):
        if self._event_filter.providedBy(event):
            print >> self.buffer, '%s.%s' % (event.__module__, event.__class__.__name__)


import sys
_ep = EventPrinter(sys.stdout)
eventPrinter = _ep.eventPrinter
channelPrinter = _ep.channelPrinter

class Null(Interface):
    """ nothing """
    __module__ = __name__


def setFilter(interface=Null, event=Null, reset=False):
    if reset:
        setFilter(Interface, Interface)
    _ep._event_filter = event
    _ep._interface = interface


def setBuffer(buffer):
    oldbuffer = _ep.buffer
    _ep.buffer = buffer
    return oldbuffer


def load_eventprint():
    from Products.Five import zcml
    from collective import testing
    zcml.load_config('printevent.zcml', testing)