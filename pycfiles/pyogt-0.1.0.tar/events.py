# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyogp/lib/base/events.py
# Compiled at: 2010-02-07 17:28:31
__doc__ = '\nContributors can be viewed at:\nhttp://svn.secondlife.com/svn/linden/projects/2008/pyogp/lib/base/trunk/CONTRIBUTORS.txt \n\n$LicenseInfo:firstyear=2008&license=apachev2$\n\nCopyright 2009, Linden Research, Inc.\n\nLicensed under the Apache License, Version 2.0.\nYou may obtain a copy of the License at:\n    http://www.apache.org/licenses/LICENSE-2.0\nor in \n    http://svn.secondlife.com/svn/linden/projects/2008/pyogp/lib/base/LICENSE.txt\n\n$/LicenseInfo$\n'
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