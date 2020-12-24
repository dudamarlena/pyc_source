# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Python/2.7/site-packages/medialog/boardfile/browser/views.py
# Compiled at: 2011-10-07 04:21:09
"""
    Exposed URLs for sending time based events.

"""
__author__ = 'Mikko Ohtamaa <mikko.ohtamaa@twinapex.com>'
__copyright__ = 'Copyright 2008 Twinapex Research'
__license__ = 'GPL'
__docformat__ = 'epytext'
import logging
from DateTime.DateTime import DateTime
from zope.event import notify
from Products.Five.browser import BrowserView
from zope.app.session.interfaces import ISession, ISessionDataContainer
from zope import component
from zope.app import zapi
from zope.app.session.session import SessionData, PersistentSessionDataContainer, RAMSessionDataContainer
from events import TickEvent
client_id = 'collective.timedevents'
package_id = 'collective.timedevents'

class TickData:
    """ Persistent information about ticking. """

    def __init__(self, interval):
        self.interval = interval
        self.last_tick = None
        return


sdc = PersistentSessionDataContainer()

class TickTriggerView(BrowserView):
    """ View that is called by Zope clock server.
    
    Clock server pulse calls this view regularly. View check whether we have 
    enough interval since the last event burst and calls event handlers.
    
    Ticking data is kept in Zope persistent session storage,
    using view url as the key.
    """
    interval = 600

    def getTickData(self):
        """ Lazily initialize run-time tick data.
        
        We need to store process shared data somewhere.
        """
        sdc.timeout = self.interval * 3
        client_id = self.context.absolute_url()
        if client_id not in sdc:
            sdc[client_id] = SessionData()
        container = sdc[client_id]
        if 'interval' not in container:
            container['interval'] = self.interval
            container['last_tick'] = None
        return container

    def getInterval(self):
        return self.getTickData()['interval']

    def setLastTick(self, time):
        self.getTickData()['last_tick'] = time

    def getLastTick(self):
        return self.getTickData()['last_tick']

    def tick(self):
        """ Perform tick event firing when needed. """
        current = DateTime()
        last = self.getLastTick()
        if not isinstance(last, DateTime):
            last = DateTime(0)
        interval = self.getInterval()
        if interval < 0:
            interval = 0
        if current.timeTime() - last.timeTime() >= 0.9 * interval:
            self.setLastTick(current)
            notify(TickEvent(current, self.getNextTickEstimation(last_tick=current, interval=interval)))

    def getNextTickEstimation(self, last_tick=None, interval=None):
        """This method tries to estimate a time when a next tick will occur.
           Then it returns a DateTime object representing that time. 
        """
        if last_tick is None:
            last_tick = DateTime(self.getLastTick())
        if interval is None:
            interval = float(self.getInterval())
        interval = interval / 86400.0
        next_tick_estimation = last_tick + interval
        return next_tick_estimation

    def __call__(self):
        self.tick()
        return 'OK'