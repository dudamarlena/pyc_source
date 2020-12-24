# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/spoon/messaging/decorators.py
# Compiled at: 2006-11-27 19:08:20
from messagingcore import SingletonMessaging

class receive(object):
    """
    The receive decorator can be used to decorate functions and static methods 
    (NOT methods of class instances) that should receive messages of a given type.
    In the case of static methods, be sure to put the staticmethod decorator first.
    
    When a message of the given type is received, the function will be called with
    (srcNodeId, message type, attached object) as the arguments to it.
    """
    __module__ = __name__

    def __init__(self, msgtype):
        """
        @param msgtype: Indicates the message type that the function will receive.
        This can be a list of msgtypes as well as just a string.
        """
        if type(msgtype) == str:
            self.msgtype = [
             msgtype]
        else:
            self.msgtype = msgtype

    def __call__(self, handler):
        messaging = SingletonMessaging.getinstance()
        for x in self.msgtype:
            messaging.registerHandler(x, handler)


handleMsg = receive