# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/wasp/interfaces.py
# Compiled at: 2008-09-17 11:14:28
from zope.interface import Interface

class IReceiveMessage(Interface):
    __module__ = __name__

    def __call__(msisdn, message_text):
        """
        This method is called to handle incoming messages.
        The implementation should do whatever is required by the
        application.

        msisdn - the msisdn that sent the incoming message

        message_text - the text of the message
        """
        pass


class INotifyMessage(Interface):
    __module__ = __name__

    def __call__(message_id, status, details):
        """
        This method is called when status notifications about a
        previously sent message are recieved.

        message_id - will be that passed in the call to the `send`
                     method

        status - will be the 
        """
        pass


class ISendMessage(Interface):
    __module__ = __name__

    def __call__(msisdn, message_text, message_id=None):
        """
        Send the message_text to the specified msisdn.
        The message_id is a unique id for this message. If supplied,
        it will be returned to any configured INotifyMessage.

        This returns either:

        True - indicating that the message has been
               successfully delivered

        False - indicating that a notification of delivery status will
                be sent.
                (NB: an IRecieveMessage must be configured in this
                     case)

        In other cases, an exception should be raised indicating the
        nature of the problem that occurred.
        """
        pass


class IProcessResponse(Interface):
    """
    Each WASP implementation should provide a utility implementing
    this interface.
    """
    __module__ = __name__

    def process(request, form, body):
        """
        This method is called by the reciever view with information
        from the request received. This should be parsed and an
        iterable returned that yields wasp.Notification and
        wasp.Message objects. For more information on these see their
        docstrings and code.
        It's acceptable to return an empty sequence or a sequence
        containing one item.
        """
        pass

    def response():
        """
        This should return a string containing the values to be
        returned by the Receiver view.
        This will need to be done in the event that the WASP
        implementation requires a specific response to any HTTP POSTs
        or GETs that it sends.
        """
        pass