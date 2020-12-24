# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/spoon/transports/transports.py
# Compiled at: 2006-11-19 22:31:45
from spoon import Serial, SpoonStream, serialprop, __SPOONLINKMSG_TAG__
from spoon import NullLogger, LMTYPE_INIT, LMTYPE_NETWORK, LMTYPE_NETWORK_PROTO
from spoon import ber
from threading import Thread

class SpoonRPCHello(Serial):
    """
    This object is sent as a very simple form of initial negotiation.
    It contains the nodeId and the protocol version (currently always
    1.)
    """
    __module__ = __name__
    nodeId = serialprop()
    version = serialprop(1)


class LinkMessage(object):
    """
    Link message is the wrapper which will contain messages sent between two directly connected nodes.
    This message just consists of a msg type (an int) and some arbitrary attachment.  The msgtype 
    determines what system will deal with the message.
    Since this is strictly for use between directly connected nodes, there's no need for src or destination
    fields.
    """
    __module__ = __name__

    def __init__(self, msgtype=None, attach=None):
        self.msgtype = msgtype
        self.attach = attach


@ber.encoder(LinkMessage)
def encode_linkmessage(fd, obj):
    ber.Tag.from_tag(__SPOONLINKMSG_TAG__, None).write(fd)
    b = ber.BERStream(fd)
    b.add(obj.msgtype)
    b.add(obj.attach)
    b._add_eof()
    return


@ber.decoder(__SPOONLINKMSG_TAG__)
def decode_linkmessage(fd, tag):
    out = LinkMessage()
    b = ber.BERStream(fd)
    out.msgtype = b.next()
    out.attach = b.next()
    if b.has_next():
        pass
    return out


class TransportException(Exception):
    __module__ = __name__


class TransportHub(object):
    """
    Where all of your transports connect to form your glorious new node.
    
    
    @cvar activeTransports: A simple list of the transports that are currently active
    @cvar links: A dict, keys are the node id of the directly connected neighbor and the values are 
    the associated transport
    @cvar nodeId: The local node id.  This must be set to the node's integer id before the spoon transport hub is started.
    The nodeId is just a network wide, unique int.  How this is determined is left as an excercise for the implementation.
    In most cases, it should probably be something that is constant for the host/program between instances.
    @type nodeId: int
    """
    __module__ = __name__
    activeTransports = []
    links = {}
    nodeId = None
    _log = NullLogger()

    @staticmethod
    def setLogger(logger):
        """
        Sets a logger object for SpoonRPC to use.
        
        This can be a python logger object, or just anything that supports that general protocol.
        It defaults to NullLogger which does nothing with the messages.  
        """
        TransportHub._log = logger

    @staticmethod
    def addTransport(t):
        """
        Must be called after a transport is initialized to initiate the spoonRPC protocol.
        
        @param t: The transport being initialized
        @return: Nothing
        @raise TransportException: If the protocol initialization fails for some reason.
        """
        hello = SpoonRPCHello()
        hello.nodeId = TransportHub.nodeId
        lmhello = LinkMessage(LMTYPE_INIT, hello)
        t.spoon.write(lmhello)
        remoteLmHello = t.spoon.read()
        remoteHello = remoteLmHello.attach
        if type(remoteLmHello) != LinkMessage or type(remoteHello) != SpoonRPCHello:
            TransportHub._log.error('Did not get proper Hello message from neighbor across transport ' + repr(t))
            raise TransportException('Did not get proper Hello message from neighbor across transport ' + repr(t))
        if TransportHub.links.has_key(remoteHello.nodeId):
            try:
                TransportHub.activeTransports.remove(TransportHub.links[remoteHello.nodeId])
            except:
                pass
            else:
                del TransportHub.links[remoteHello.nodeId]
        t.nodeId = remoteHello.nodeId
        TransportHub.links[remoteHello.nodeId] = t
        TransportHub.activeTransports.append(t)
        tNetwork = t.getNetwork()
        if tNetwork:
            tNetwork.addTransport(t, t.nodeId)

    @staticmethod
    def removeTransport(t):
        """
        Must be called after a transport has been made inactive.
        
        """
        if not TransportHub.links.has_key(t.nodeId):
            TransportHub._log.warn("Removing transport for nodeId %d and it wasn't in the links dict." % t.nodeId)
            raise TransportException("Removing transport for nodeId %d and it wasn't in the links dict." % t.nodeId)
        del TransportHub.links[t.nodeId]
        TransportHub.activeTransports.remove(t)
        t.getNetwork().removeTransport(t)