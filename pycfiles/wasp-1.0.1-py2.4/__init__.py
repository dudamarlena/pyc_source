# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/wasp/__init__.py
# Compiled at: 2008-09-17 11:14:28
from interfaces import ISendMessage, IReceiveMessage, INotifyMessage, IProcessResponse
from zope.component import getUtility, queryAdapter
from zope.publisher.browser import BrowserView

def send(msisdn, message_text, message_id=None):
    return getUtility(ISendMessage)(msisdn, message_text, message_id)


class Receiver(BrowserView):
    __module__ = __name__

    def __call__(self):
        bodyStream = getattr(self.request, 'bodyStream', None)
        if bodyStream is None:
            body = self.request.get('BODY', '')
        else:
            body = self.request.bodyStream.read()
        utility = getUtility(IProcessResponse)
        for event in utility.process(self.request, self.request.form, body):
            adapter = queryAdapter(self.context, event.interface)
            if adapter is not None:
                adapter(**event.__dict__)
            else:
                getUtility(event.interface)(**event.__dict__)

        return utility.response()


class Notification:
    """
    A notification object used to dispatch notifications from an
    IProcessResponse utility to INotifyMessage utilities or adapters.

    message_id - the message_id passed to the `send` method

    status - one of the statuses in wasp.status

    details - a string giving more information about why the status
              was returned. In the case of errors, this should contain
              the full error message returned from the WASP.
              If the status is wasp.status.Delivered then this may be
              an empty string.
    """
    __module__ = __name__
    interface = INotifyMessage

    def __init__(self, message_id, status, details):
        self.message_id = message_id
        self.status = status
        self.details = details


class Message:
    """
    A message object used to dispatch messages recieved by an
    IProcessResponse utility to IRecieveMessage utilities or adapters.

    msisdn - the msisdn the message was recieved to

    message_text - the text of the recieved message.
    """
    __module__ = __name__
    interface = IReceiveMessage

    def __init__(self, msisdn, message_text):
        self.msisdn = msisdn
        self.message_text = message_text


class SendException(Exception):
    """
    An exception to raise from within an ISendMessage implementation's
    __call__ method when something goes wrong.
    """
    __module__ = __name__