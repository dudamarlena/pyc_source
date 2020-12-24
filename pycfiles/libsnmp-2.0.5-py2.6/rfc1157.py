# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/libsnmp/rfc1157.py
# Compiled at: 2008-10-18 18:59:45
import logging, debug
log = logging.getLogger('rfc1157')
from rfc1155 import *
asnTagNumbers['Get'] = 0
asnTagNumbers['GetNext'] = 1
asnTagNumbers['Response'] = 2
asnTagNumbers['Set'] = 3
asnTagNumbers['Trap'] = 4

class ErrorStatus(Integer):
    """ Error Status
    """
    errString = {0: 'No Error', 
       1: 'Response message would have been too large', 
       2: 'There is no such variable name in this MIB', 
       3: 'The value given has the wrong type', 
       4: 'Object is Read Only', 
       5: 'An unknown error occurred'}
    errNum = {'noError': 0, 
       'tooBig': 1, 
       'noSuchName': 2, 
       'badValue': 3, 
       'readOnly': 4, 
       'genErr': 5}

    def __str__(self):
        """ Return a nicer looking error
        """
        return '%d: %s' % (self.value, self.errString[self.value])

    def enum(self, num=None):
        """
        Return the stringified version of my enum.
        If a specific number is passed in, use that,
        otherwise, use my current value.
        """
        if num is None:
            num = self.value
        return self.errNum(num)


class VarBind(Sequence):
    """ Variable Binding
        This binds a name to an object
    """

    def __init__(self, name=None, value=None):
        if name:
            if not isinstance(name, ObjectID):
                raise ValueError('name must be an ObjectID')
        if value:
            if not isinstance(value, Asn1Object):
                raise ValueError('name must be an Asn1Object')
        self.objectID = name
        self.objectValue = value
        Sequence.__init__(self, [self.objectID, self.objectValue])


class VarBindList(SequenceOf):
    """ A Sequence of VarBinds
    """

    def __init__(self, value=[]):
        SequenceOf.__init__(self, VarBind, value)


class Message(Sequence):
    """ A Message is the base comms type for all SNMP messages
    """

    def __init__(self, version=0, community='public', data=None):
        Sequence.__init__(self)
        self.version = Integer(version)
        self.community = OctetString(community)
        self.data = data

    def __str__(self):
        result = '[%s, ' % self.version
        result += '%s, ' % self.community
        result += '%s]' % self.data
        return result

    def encodeContents(self):
        self.value = []
        self.value.append(self.version)
        self.value.append(self.community)
        self.value.append(self.data)
        return Sequence.encodeContents(self)

    def decode(self, stream):
        objectList = Sequence().decode(stream)
        if len(objectList) != 1:
            raise MessageError('Malformed Message: More than one object decoded.' % len(self.value))
        if len(objectList[0]) != 3:
            raise MessageError('Malformed Message: Incorrect sequence length %d' % len(self.value))
        self.version = objectList[0][0]
        self.community = objectList[0][1]
        self.data = objectList[0][2]
        return self


class MessageError(Exception):

    def __init__(self, args=None):
        self.args = args


class PDU(Sequence):
    """ Base class for a non-trap PDU
    """
    asnTagClass = asnTagClasses['CONTEXT']

    def __init__(self, requestID=0, errorStatus=0, errorIndex=0, varBindList=[]):
        """ __init__ allows you to create a new object with no arguments,
            arguments of the class ultimately desired (eg Integer)
            or, to make like easier, it will convert basic strings and ints
            into the ultimately desired objects.
        """
        Sequence.__init__(self)
        self.requestID = Integer(requestID)
        self.errorStatus = ErrorStatus(errorStatus)
        self.errorIndex = Integer(errorIndex)
        self.varBindList = VarBindList(varBindList)
        self.value = [
         self.requestID, self.errorStatus, self.errorIndex, self.varBindList]

    def decodeContents(self, stream):
        """ Decode into a Get PDU Object
        """
        objectList = Sequence.decodeContents(self, stream)
        if len(self.value) != 4:
            raise PDUError('Malformed PDU: Incorrect length %d' % len(self.value))
        myVarList = VarBindList()
        for item in objectList[3]:
            myVarList.append(VarBind(item[0], item[1]))

        return self.__class__(int(objectList[0]), int(objectList[1]), int(objectList[2]), myVarList)


class PDUError(Exception):

    def __init__(self, args=None):
        self.args = args


class Get(PDU):
    """ A Get Request PDU
    """
    asnTagNumber = asnTagNumbers['Get']


class GetNext(PDU):
    """ A GetNext PDU
    """
    asnTagNumber = asnTagNumbers['GetNext']


class Response(PDU):
    """ A Response PDU
    """
    asnTagNumber = asnTagNumbers['Get']


class Set(PDU):
    """ A Set PDU
    """
    asnTagNumber = asnTagNumbers['Set']


class GenericTrap(Integer):
    """
    Generic Trap type
    """
    genericTraps = {0: 'coldStart', 
       1: 'warmStart', 
       2: 'linkDown', 
       3: 'linkUp', 
       4: 'authenticationFailure', 
       5: 'egpNeighborLoss', 
       6: 'enterpriseSpecific'}

    def __str__(self):
        """ Return an informative string instead of just a number
        """
        return '%s: %d (%s)' % (self.__class__.__name__, self.value, self.genericTraps[self.value])

    def enum(self, num=None):
        """
        Return the stringified version of my enum.
        If a specific number is passed in, use that,
        otherwise, use my current value.
        """
        if num is None:
            num = self.value
        return self.genericTraps[num]


class TrapPDU(Sequence):
    """ A Trap PDU
    """
    asnTagClass = asnTagClasses['CONTEXT']
    asnTagNumber = asnTagNumbers['Trap']

    def __init__(self, enterprise=None, agentAddr=None, genericTrap=None, specificTrap=None, timestamp=None, varBindList=None):
        Sequence.__init__(self)
        self.enterprise = enterprise
        self.agentAddr = agentAddr
        self.genericTrap = genericTrap
        self.specificTrap = specificTrap
        self.timestamp = timestamp
        self.varBindList = varBindList
        self.value = []
        self.value.append(self.enterprise)
        self.value.append(self.agentAddr)
        self.value.append(self.genericTrap)
        self.value.append(self.specificTrap)
        self.value.append(self.timestamp)
        self.value.append(self.varBindList)

    def decodeContents(self, stream):
        """ Decode into a Get PDU Object
        """
        objectList = Sequence.decodeContents(self, stream)
        if len(self.value) != 6:
            raise PDUError('Malformed TrapPDU: Incorrect length %d' % len(self.value))
        myVarList = VarBindList()
        for item in objectList[5]:
            myVarList.append(VarBind(item[0], item[1]))

        return self.__class__(objectList[0], objectList[1], GenericTrap(int(objectList[2])), objectList[3], objectList[4], myVarList)


tagDecodeDict[160] = Get
tagDecodeDict[161] = GetNext
tagDecodeDict[162] = Response
tagDecodeDict[163] = Set
tagDecodeDict[164] = TrapPDU