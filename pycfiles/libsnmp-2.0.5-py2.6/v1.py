# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/libsnmp/v1.py
# Compiled at: 2008-10-18 18:59:45
import socket, select, logging, Queue, time, os, asyncore
from libsnmp import debug
from libsnmp import asynrole
from libsnmp.rfc1157 import *
log = logging.getLogger('v1.SNMP')
log.setLevel(logging.INFO)

class SNMP(asynrole.manager):
    nextRequestID = 0

    def __init__(self, interface=('0.0.0.0', 0), queueEmpty=None, trapCallback=None, timeout=0.25):
        """ Create a new SNMPv1 object bound to localaddr
            where localaddr is an address tuple of the form
            ('server', port)
            queueEmpty is a callback of what to do if I run out
            of stuff to do. Default is to wait for more stuff.
        """
        self.queueEmpty = queueEmpty
        self.outbound = Queue.Queue()
        self.callbacks = {}
        self.trapCallback = trapCallback
        asynrole.manager.__init__(self, (self.receiveData, None), interface=interface, timeout=timeout)
        try:
            pass
        except:
            raise

        return

    def assignRequestID(self):
        """ Assign a unique requestID 
        """
        reqID = self.nextRequestID
        self.nextRequestID += 1
        return reqID

    def createGetRequestPDU(self, varbindlist):
        reqID = self.assignRequestID()
        pdu = Get(reqID, varBindList=varbindlist)
        return pdu

    def createGetNextRequestPDU(self, varbindlist):
        reqID = self.assignRequestID()
        pdu = GetNext(reqID, varBindList=varbindlist)
        return pdu

    def createGetRequestMessage(self, oid, community='public'):
        """ Creates a message object from a pdu and a
            community string.
        """
        objID = ObjectID(oid)
        val = Null()
        varbindlist = VarBindList([VarBind(objID, val)])
        pdu = self.createGetRequestPDU(varbindlist)
        return Message(community=community, data=pdu)

    def createGetNextRequestMessage(self, varbindlist, community='public'):
        """ Creates a message object from a pdu and a
            community string.
        """
        pdu = self.createGetNextRequestPDU(varbindlist)
        return Message(community=community, data=pdu)

    def createTrapMessage(self, pdu, community='public'):
        """ Creates a message object from a pdu and a
            community string.
        """
        return Message(community=community, data=pdu)

    def createTrapPDU(self, varbindlist, enterprise='.1.3.6.1.4', agentAddr=None, genericTrap=6, specificTrap=0):
        """ Creates a Trap PDU object from a list of strings and integers
            along with a varBindList to make it a bit easier to build a Trap.
        """
        ent = ObjectID(enterprise)
        if not agentAddr:
            agentAddr = self.getsockname()[0]
        agent = NetworkAddress(agentAddr)
        gTrap = GenericTrap(genericTrap)
        sTrap = Integer(specificTrap)
        ts = TimeTicks(self.getSysUptime())
        pdu = TrapPDU(ent, agent, gTrap, sTrap, ts, varbindlist)
        return pdu

    def snmpGet(self, oid, remote, callback, community='public'):
        """ snmpGet issues an SNMP Get Request to remote for
            the object ID oid 
            remote is a tuple of (host, port)
            oid is a dotted string eg: .1.2.6.1.0.1.1.3.0
        """
        msg = self.createGetRequestMessage(oid, community)
        self.outbound.put((msg, remote))
        self.callbacks[int(msg.data.requestID)] = callback
        return msg.data.requestID

    def snmpGetNext(self, varbindlist, remote, callback, community='public'):
        """ snmpGetNext issues an SNMP Get Next Request to remote for
            the varbindlist that is passed in. It is assumed that you
            have either built a varbindlist yourself or just pass
            one in that was previously returned by an snmpGet or snmpGetNext
        """
        msg = self.createGetNextRequestMessage(varbindlist, community)
        self.outbound.put((msg, remote))
        self.callbacks[int(msg.data.requestID)] = callback
        return msg.data.requestID

    def snmpSet(self, varbindlist, remote, callback, community='public'):
        """ An snmpSet requires a bit more up front smarts, in that
            you need to pass in a varbindlist of matching OIDs and
            values so that the value type matches that expected for the
            OID. This library does not care about any of that stuff.

        """
        reqID = self.assignRequestID()
        pdu = GetNext(reqID, varBindList=varbindlist)
        msg = Message(community=community, data=pdu)
        self.outbound.put((msg, remote))
        self.callbacks[int(msg.data.requestID)] = callback
        return msg.data.requestID

    def snmpTrap(self, remote, trapPDU, community='public'):
        """ Queue up a trap for sending
        """
        msg = self.createTrapMessage(trapPDU, community)
        self.outbound.put((msg, remote))

    def createSetRequestMessage(self, varBindList, community='public'):
        """ Creates a message object from a pdu and a
            community string.
        """
        pass

    def receiveData(self, manager, cb_ctx, (data, src), (exc_type, exc_value, exc_traceback)):
        """ This method should be called when data is received
            from a remote host.
        """
        if exc_type is not None:
            raise exc_type(exc_value)
        try:
            msg = Message().decode(data)
            if msg.version == 0:
                log.debug('Detected SNMPv1 message')
            else:
                log.error('Unknown message version %d detected' % msg.version)
                log.error('version is a %s' % msg.version())
                raise ValueError('Unknown message version %d detected' % msg.version)
            if isinstance(msg.data, PDU):
                self.callbacks[int(msg.data.requestID)](self, msg)
                del self.callbacks[int(msg.data.requestID)]
            elif isinstance(msg.data, TrapPDU):
                log.debug('Detected an inbound Trap')
                self.trapCallback(self, msg)
            else:
                log.debug('Unknown message type')
        except Exception, e:
            log.error('Exception in receiveData: %s' % e)
            raise

        return

    def enterpriseOID(self, partialOID):
        """ A convenience method to automagically prepend the
            'enterprise' prefix to the partial OID
        """
        return '.1.3.6.1.2.1.' + partialOID

    def run(self):
        """ Listen for incoming request thingies
            and send pending requests
        """
        while True:
            try:
                request = self.outbound.get(0)
                self.send(request[0].encode(), request[1])
            except Queue.Empty:
                if self.queueEmpty is not None:
                    self.queueEmpty(self)
                self.poll()
                time.sleep(0.1)

        return

    def getSysUptime(self):
        """ This is a pain because of system dependence
            Each OS has a different way of doing this and I
            cannot find a Python builtin that will do it.
        """
        try:
            uptime = open('/proc/uptime').read().split()
            upsecs = int(float(uptime[0]) * 100)
            return upsecs
        except:
            return 0