# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyogp/lib/base/message/message_handler.py
# Compiled at: 2010-02-07 17:28:31
__doc__ = '\nContributors can be viewed at:\nhttp://svn.secondlife.com/svn/linden/projects/2008/pyogp/lib/base/trunk/CONTRIBUTORS.txt \n\n$LicenseInfo:firstyear=2008&license=apachev2$\n\nCopyright 2009, Linden Research, Inc.\n\nLicensed under the Apache License, Version 2.0.\nYou may obtain a copy of the License at:\n    http://www.apache.org/licenses/LICENSE-2.0\nor in \n    http://svn.secondlife.com/svn/linden/projects/2008/pyogp/lib/base/LICENSE.txt\n\n$/LicenseInfo$\n'
from logging import getLogger
from pyogp.lib.base.events import Event
from pyogp.lib.base.settings import Settings
logger = getLogger('...message.message_handler')

class MessageHandler(object):
    """ general class handling individual messages """
    __module__ = __name__

    def __init__(self, settings=None):
        """ i do nothing """
        if settings != None:
            self.settings = settings
        else:
            from pyogp.lib.base.settings import Settings
            self.settings = Settings()
        self.handlers = {}
        return

    def register(self, message_name):
        if self.settings.LOG_VERBOSE:
            logger.debug('Creating a monitor for %s' % message_name)
        return self.handlers.setdefault(message_name, MessageHandledNotifier(message_name, self.settings))

    def is_message_handled(self, message_name):
        """ if the message is being monitored, return True, otherwise, return False 

        this can allow us to skip parsing inbound messages if no one is watching a particular one
        """
        try:
            handler = self.handlers[message_name]
            return True
        except KeyError:
            return False

    def handle(self, message):
        """ essentially a case statement to pass messages to event notifiers in the form of self attributes """
        try:
            handler = self.handlers[message.name]
            if len(handler) > 0:
                if self.settings.LOG_VERBOSE and not (self.settings.UDP_SPAMMERS and self.settings.DISABLE_SPAMMERS):
                    logger.debug('Handling message : %s' % message.name)
                handler(message)
        except KeyError:
            pass


class MessageHandledNotifier(object):
    """ pseudo subclassing the Event class to treat the message like an event """
    __module__ = __name__

    def __init__(self, message_name, settings):
        self.event = Event()
        self.message_name = message_name
        self.settings = settings

    def subscribe(self, *args, **kwdargs):
        self.event.subscribe(*args, **kwdargs)

    def received(self, message):
        self.event(message)

    def unsubscribe(self, *args, **kwdargs):
        self.event.unsubscribe(*args, **kwdargs)
        if self.settings.LOG_VERBOSE:
            logger.debug('Removed the monitor for %s by %s' % (args, kwdargs))

    def __len__(self):
        return len(self.event)

    __call__ = received