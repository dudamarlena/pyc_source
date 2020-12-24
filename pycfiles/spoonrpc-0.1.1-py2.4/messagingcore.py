# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/spoon/messaging/messagingcore.py
# Compiled at: 2006-11-22 16:27:32
from spoon import NMTYPE_MESSAGING

class Messaging(object):
    """
    This is the main messaging class that implements the basic functionality for Spoon.
    Messaging implementations that need specific functionality (such as reliablility) will
    probably want to subclass from this.
    
    There may be multiple instances of Messaging per python process, however there should only be one per
    network to which a node is a member.  There may be a case where one would want a single Messaging instance
    shared between networks however, and as long as the node ids on the networks do not overlap, you shouldn't have
    any problems.
    
    You cannot use the acceptMsg decorator with this, for that you have to use the SingletonMessaging class.
    To register handlers with instances of Messaging, you must use the registerHandler method on
    the Messaging instance.
    """
    __module__ = __name__

    def __init__(self, network=None):
        self.handlers = {}
        self.network = network
        if network:
            self.network.nmtypes[NMTYPE_MESSAGING] = self

    def registerHandler(self, msgtype, handler):
        handlers = self.handlers.get(msgtype, None)
        if handlers:
            handlers.append(handler)
        else:
            self.handlers[msgtype] = [
             handler]
        return

    def unregisterHandler(self, msgtype, handler):
        handlers = self.handlers.get(msgtype, None)
        if handlers:
            try:
                handlers.remove(handler)
            except:
                pass

        return

    def handleMessage(self, src, msg):
        """
        Calls the all handlers for the given message.
        @param src: The source node of the message
        @param msg: A list containing the message type, and the attached object.
        """
        handlers = self.handlers.get(msg[0], [])
        for handler in handlers:
            handler(src, msg[0], msg[1])

    def setNetwork(self, network):
        self.network = network
        self.network.nmtypes[NMTYPE_MESSAGING] = self

    def send(self, dst, messageStr, obj):
        """
        Sends a Messaging message (not just a NetMessage) to the 
        destination node.
        @param dst: Destination node id
        @param messageStr: A string describing the message type.
        @param obj: Some object attached the net message.
        """
        self.network.sendNetMsg(dst, NMTYPE_MESSAGING, (messageStr, obj))


class SingletonMessaging(Messaging):
    """
    For convinience this is a singleton version of the Messaging system.
    This can be used when the node will only have one Messaging system
    throughout the life of the process.  Furthermore, if this is the case
    you can use the function/static method decorator acceptMsg with this.
    """
    __module__ = __name__
    singleton = None

    @staticmethod
    def getinstance():
        if SingletonMessaging.singleton:
            return SingletonMessaging.singleton
        else:
            SingletonMessaging.singleton = SingletonMessaging()
            return SingletonMessaging.singleton

    @staticmethod
    def hasinstance():
        return SingletonMessaging.singleton != None


def send(dst, messageStr, obj):
    """
    Shortcut for calling send on the SingletonMessaging class.
    @param dst: Destination node id
    @param messageStr: A string describing the message type.
    @param obj: Some object attached the net message.
    """
    SingletonMessaging.getinstance().send(dst, messageStr, obj)