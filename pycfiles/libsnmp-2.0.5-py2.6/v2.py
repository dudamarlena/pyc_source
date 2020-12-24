# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/libsnmp/v2.py
# Compiled at: 2010-01-29 18:45:51
import logging, traceback
from libsnmp import debug
from libsnmp import rfc1155
from libsnmp import rfc1157
from libsnmp import rfc1902
from libsnmp import rfc1905
from libsnmp import v1
log = logging.getLogger('v2.SNMP')
log.setLevel(logging.INFO)

class SNMP(v1.SNMP):

    def createGetRequestPDU(self, varbindlist):
        reqID = self.assignRequestID()
        pdu = rfc1905.Get(reqID, varBindList=varbindlist)
        return pdu

    def createGetNextRequestPDU(self, varbindlist):
        reqID = self.assignRequestID()
        pdu = rfc1905.GetNext(reqID, varBindList=varbindlist)
        return pdu

    def createGetRequestMessage(self, oidlist, community='public'):
        """
        Creates a message object from a pdu and a
        community string.
        @param oidlist: a list of oids to place in the message.
        """
        varbinds = []
        for oid in oidlist:
            objID = rfc1155.ObjectID(oid)
            val = rfc1155.Null()
            varbinds.append(rfc1157.VarBind(objID, val))

        varbindlist = rfc1905.VarBindList(varbinds)
        pdu = self.createGetRequestPDU(varbindlist)
        return rfc1905.Message(community=community, data=pdu)

    def createGetNextRequestMessage(self, varbindlist, community='public'):
        """ Creates a message object from a pdu and a
            community string.
        """
        pdu = self.createGetNextRequest(varbindlist)
        return rfc1905.Message(community=community, data=pdu)

    def createTrapMessage(self, pdu, community='public'):
        """ Creates a message object from a pdu and a
            community string.
        """
        return rfc1905.Message(community=community, data=pdu)

    def createTrap(self, varbindlist, enterprise='.1.3.6.1.4', agentAddr=None, genericTrap=6, specificTrap=0):
        """ Creates a Trap PDU object from a list of strings and integers
            along with a varBindList to make it a bit easier to build a Trap.
        """
        ent = rfc1155.ObjectID(enterprise)
        if not agentAddr:
            agentAddr = self.getsockname()[0]
        agent = rfc1155.NetworkAddress(agentAddr)
        gTrap = rfc1157.GenericTrap(genericTrap)
        sTrap = rfc1155.Integer(specificTrap)
        ts = rfc1155.TimeTicks(self.getSysUptime())
        pdu = rfc1157.TrapPDU(ent, agent, gTrap, sTrap, ts, varbindlist)
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
        pdu = rfc1157.GetNextRequestPDU(reqID, varBindList=varbindlist)
        msg = rfc1905.Message(community=community, data=pdu)
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
            msg = rfc1905.Message().decode(data)
            if msg.version == 0:
                log.debug('Detected SNMPv1 message')
            elif msg.version == 1:
                log.debug('Detected SNMPv2 message')
            else:
                log.error('Unknown message version %d detected' % msg.version)
                log.error('version is a %s' % msg.version())
                raise ValueError('Unknown message version %d detected' % msg.version)
            if isinstance(msg.data, rfc1157.PDU):
                self.callbacks[int(msg.data.requestID)](self, msg)
                del self.callbacks[int(msg.data.requestID)]
            elif isinstance(msg.data, rfc1157.TrapPDU):
                log.debug('Detected an inbound Trap')
                self.trapCallback(self, msg)
            else:
                log.debug('Unknown message type')
        except Exception, e:
            log.error('Exception in receiveData: %s' % e)
            traceback.print_exc()

        return