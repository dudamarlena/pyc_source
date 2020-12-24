# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyogp/lib/base/events.py
# Compiled at: 2010-02-07 17:28:31
"""
Contributors can be viewed at:
http://svn.secondlife.com/svn/linden/projects/2008/pyogp/lib/base/trunk/CONTRIBUTORS.txt 

$LicenseInfo:firstyear=2008&license=apachev2$

Copyright 2009, Linden Research, Inc.

Licensed under the Apache License, Version 2.0.
You may obtain a copy of the License at:
    http://www.apache.org/licenses/LICENSE-2.0
or in 
    http://svn.secondlife.com/svn/linden/projects/2008/pyogp/lib/base/LICENSE.txt

$/LicenseInfo$
"""
from logging import getLogger
import traceback
logger = getLogger('utilities.events')

class Event(object):
    """ an object containing data which will be passed out to all subscribers """
    __module__ = __name__

    def __init__(self):
        self.subscribers = []

    def subscribe(self, handler, *args, **kwargs):
        """ establish the subscribers (handlers) to this event """
        self.subscribers.append((handler, args, kwargs))
        return self

    def unsubscribe(self, handler, *args, **kwargs):
        """ remove the subscriber (handler) to this event """
        try:
            self.subscribers.remove((handler, args, kwargs))
        except:
            raise ValueError("Handler '%s' is not subscribed to this event." % s(handler))

        return self

    def notify(self, args):
        for (instance, inner_args, kwargs) in self.subscribers:
            try:
                instance(args, *inner_args, **kwargs)
            except Exception, error:
                traceback.print_exc()
                logger.warning('Error in event firing module')
                raise

    def getSubscriberCount(self):
        return len(self.subscribers)

    def clearSubscribers(self):
        self.subscribers.clear()
        return self

    def getSubscribers(self):
        return self.subscribers

    __iadd__ = subscribe
    __isub__ = unsubscribe
    __call__ = notify
    __len__ = getSubscriberCount