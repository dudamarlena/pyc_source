# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Python/2.7/site-packages/medialog/boardfile/browser/events.py
# Compiled at: 2011-10-07 04:21:09
"""
    Time based events
    A lot of code taken from collective.timedevents
    Mikko Ohtamaa <mikko.ohtamaa@twinapex.com

"""
__author__ = 'spen Moe-Nilssen <espen@medialog.no>'
__license__ = 'GPL'
__docformat__ = 'epytext'
import logging, zope
from DateTime import DateTime
from zope.component import adapter
from zope.app.component.hooks import getSite
from interfaces import ITickEvent
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.log import logger
triggered_count = 0

class TickEvent(object):
    """This class implements the ITickEvent interface.
    """
    zope.interface.implements(ITickEvent)

    def __init__(self, date_time, next_tick):
        self.date_time = DateTime(date_time)
        self.next_tick = DateTime(next_tick)


@adapter(ITickEvent)
def tick_logger(tick_event):
    """This function is a handler for the ITickEvent. Its purpose is to log all
       ticks.
    """
    l = logging.getLogger('timedevents')
    l.info('(%s) TICK detected...' % tick_event.date_time.ISO())


class TransitionTriggerTicker:
    """ Perform automatic transitions for workflows after certain amount of time is reached in some content attribute.
    """
    time_variable = 'submit_time'

    def __call__(self, event):
        """

        @param event: zope event object
        """
        global triggered_count
        now = event.date_time
        delta = 20
        site = getSite()
        logger.debug('Running timed workflow transitions checks at %s, site is: %s, transition is %s' % (str(now), str(site), self.transition))
        pct = getToolByName(site, 'portal_catalog')
        wf = getToolByName(site, 'portal_workflow')
        query = {}
        query['portal_type'] = 'PublicationRequest'
        query['review_state'] = self.state
        catalog_data = pct.unrestrictedSearchResults(**query)
        for item in catalog_data:
            obj = item.getObject()
            status = wf.getStatusOf(self.workflow, obj)
            logger.debug('Checking autotransition for:' + str(obj))
            if now >= status[self.time_variable] + self.delta:
                logger.info('Triggering auto transition for:' + str(obj) + ' state:' + status['review_state'] + ' transition:' + self.transition)
                wf.doActionFor(obj, self.transition)
                triggered_count += 1


class AutoExpireDocument(TransitionTriggerTicker):
    """ Define a sample time based trigger. """
    workflow = 'multiapprove_workflow'
    state = 'pending'
    transition = 'auto_publish'
    pt = 'Boardfile'
    delta = 20


auto_expire = AutoExpireDocument()