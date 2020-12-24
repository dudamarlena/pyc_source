# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\PyTrinamic\connections\tmcl_interface.py
# Compiled at: 2019-11-06 08:41:37
# Size of source mod 2**32: 9279 bytes
"""
Created on 27.05.2019

@author: LH
"""
from PyTrinamic.TMCL import TMCL_Request, TMCL_Command, TMCL_Reply
from PyTrinamic.helpers import TMC_helpers

class tmcl_interface:
    __doc__ = '\n    This class is a base class for sending TMCL commands over a communication\n    interface.\n\n    Each instance of this class represents one TMCL host. The bus connection for\n    the TMCL communication is represented by a subclass inheriting this base\n    class. An application with multiple busses should therefore use subclasses\n    for all types of busses (e.g. one USB TMCL interface and one serial TMCL\n    interface) and create exactly one instance of one of those subclasses per\n    bus.\n\n    A subclass is required to override the following functions:\n        _send(self, hostID, moduleID, data)\n        _recv(self, hostID, moduleID)\n\n    A subclass may use the boolean _debug attribute to toggle printing further\n    debug output.\n\n    A subclass may read the _HOST_ID and _MODULE_ID parameters.\n    '

    def __init__(self, hostID=2, defaultModuleID=1, debug=False):
        """
        Parameters:
            hostID:
                Type: int, optional, default value: 2
                The ID of the TMCL host. This ID is the same for each module
                when communicating with multiple modules.
            moduleID:
                Type: int, optional, default value: 1
                The default module ID to use when no ID is given to any of the
                tmcl_interface functions. When only communicating with one
                module a script can omit the moduleID for all TMCL interface
                calls by declaring this default value once at the start.
            debug:
                Type: bool, optional, default: False
                A switch for enabling debug mode. Can be changed with
                enableDebug(). In debug mode all sent and received TMCL packets
                get dumped to stdout. The boolean _debug attribute holds the
                current state of debug mode - subclasses may read it to print
                further debug output.
        """
        if not type(hostID) == type(defaultModuleID) == int:
            raise TypeError
        else:
            if not 0 <= hostID < 256:
                raise ValueError('Incorrect Host ID value')
            if not 0 <= defaultModuleID < 256:
                raise ValueError('Incorrect defaultModule ID value')
            assert type(debug) == bool
        self._HOST_ID = hostID
        self._MODULE_ID = defaultModuleID
        self._debug = debug

    def _send(self, hostID, moduleID, data):
        """
        Send the bytearray [data] representing a TMCL command. The length of
        [data] is 9. The hostID and moduleID parameters may be used for extended
        addressing options available on the implemented communication interface.
        """
        raise NotImplementedError('The TMCL interface requires an implementation of the _send() function')

    def _recv(self, hostID, moduleID):
        """
        Receive a TMCL reply and return it as a bytearray. The length of the
        returned byte array is 9. The hostID and moduleID parameters may be used
        for extended addressing options available on the implemented
        communication interface.
        """
        raise NotImplementedError('The TMCL interface requires an implementation of the _recv() function')

    def enableDebug(self, enable):
        """
        Set the debug mode, which dumps all TMCL datagrams written and read.
        """
        if type(enable) != bool:
            raise TypeError('Expected boolean value')
        self._debug = enable

    def send--- This code section failed: ---

 L. 101         0  LOAD_GLOBAL              type
                2  LOAD_FAST                'opcode'
                4  CALL_FUNCTION_1       1  '1 positional argument'
                6  LOAD_GLOBAL              type
                8  LOAD_FAST                'opType'
               10  CALL_FUNCTION_1       1  '1 positional argument'
               12  DUP_TOP          
               14  ROT_THREE        
               16  COMPARE_OP               ==
               18  POP_JUMP_IF_FALSE    56  'to 56'
               20  LOAD_GLOBAL              type
               22  LOAD_FAST                'motor'
               24  CALL_FUNCTION_1       1  '1 positional argument'
               26  DUP_TOP          
               28  ROT_THREE        
               30  COMPARE_OP               ==
               32  POP_JUMP_IF_FALSE    56  'to 56'
               34  LOAD_GLOBAL              type
               36  LOAD_FAST                'value'
               38  CALL_FUNCTION_1       1  '1 positional argument'
               40  DUP_TOP          
               42  ROT_THREE        
               44  COMPARE_OP               ==
               46  POP_JUMP_IF_FALSE    56  'to 56'
               48  LOAD_GLOBAL              int
               50  COMPARE_OP               ==
               52  POP_JUMP_IF_TRUE     66  'to 66'
               54  JUMP_FORWARD         58  'to 58'
             56_0  COME_FROM            46  '46'
             56_1  COME_FROM            32  '32'
             56_2  COME_FROM            18  '18'
               56  POP_TOP          
             58_0  COME_FROM            54  '54'

 L. 102        58  LOAD_GLOBAL              TypeError
               60  LOAD_STR                 'Expected integer values'
               62  CALL_FUNCTION_1       1  '1 positional argument'
               64  RAISE_VARARGS_1       1  'exception instance'
             66_0  COME_FROM            52  '52'

 L. 105        66  LOAD_FAST                'moduleID'
               68  POP_JUMP_IF_TRUE     76  'to 76'

 L. 106        70  LOAD_FAST                'self'
               72  LOAD_ATTR                _MODULE_ID
               74  STORE_FAST               'moduleID'
             76_0  COME_FROM            68  '68'

 L. 108        76  LOAD_GLOBAL              TMCL_Request
               78  LOAD_FAST                'moduleID'
               80  LOAD_FAST                'opcode'
               82  LOAD_FAST                'opType'
               84  LOAD_FAST                'motor'
               86  LOAD_FAST                'value'
               88  CALL_FUNCTION_5       5  '5 positional arguments'
               90  STORE_FAST               'request'

 L. 110        92  LOAD_FAST                'self'
               94  LOAD_ATTR                _debug
               96  POP_JUMP_IF_FALSE   106  'to 106'

 L. 111        98  LOAD_FAST                'request'
              100  LOAD_METHOD              dump
              102  CALL_METHOD_0         0  '0 positional arguments'
              104  POP_TOP          
            106_0  COME_FROM            96  '96'

 L. 114       106  LOAD_FAST                'self'
              108  LOAD_METHOD              _send
              110  LOAD_FAST                'self'
              112  LOAD_ATTR                _HOST_ID
              114  LOAD_FAST                'moduleID'
              116  LOAD_FAST                'request'
              118  LOAD_METHOD              toBuffer
              120  CALL_METHOD_0         0  '0 positional arguments'
              122  CALL_METHOD_3         3  '3 positional arguments'
              124  POP_TOP          

 L. 117       126  LOAD_GLOBAL              TMCL_Reply
              128  LOAD_FAST                'self'
              130  LOAD_METHOD              _recv
              132  LOAD_FAST                'self'
              134  LOAD_ATTR                _HOST_ID
              136  LOAD_FAST                'moduleID'
              138  CALL_METHOD_2         2  '2 positional arguments'
              140  CALL_FUNCTION_1       1  '1 positional argument'
              142  STORE_FAST               'reply'

 L. 119       144  LOAD_FAST                'self'
              146  LOAD_ATTR                _debug
              148  POP_JUMP_IF_FALSE   158  'to 158'

 L. 120       150  LOAD_FAST                'reply'
              152  LOAD_METHOD              dump
              154  CALL_METHOD_0         0  '0 positional arguments'
              156  POP_TOP          
            158_0  COME_FROM           148  '148'

 L. 122       158  LOAD_FAST                'reply'
              160  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def sendBoot(self, moduleID=None):
        """
        Send the command for entering bootloader mode. This TMCL command does
        result in a reply.
        """
        if not moduleID:
            moduleID = self._MODULE_ID
        request = TMCL_RequestmoduleIDTMCL_Command.BOOT1291462746533334
        if self._debug:
            request.dump
        self._sendself._HOST_IDmoduleIDrequest.toBuffer

    def getVersionString(self, moduleID=None):
        """
        Request the ASCII version string.
        """
        reply = self.send(TMCL_Command.GET_FIRMWARE_VERSION, 0, 0, 0, moduleID)
        return reply.versionString

    def parameter(self, pCommand, pType, pAxis, pValue, moduleID=None, signed=False):
        value = self.send(pCommand, pType, pAxis, pValue, moduleID).value
        if signed:
            return TMC_helpers.toSigned32(value)
        return value

    def setParameter(self, pCommand, pType, pAxis, pValue, moduleID=None):
        return self.send(pCommand, pType, pAxis, pValue, moduleID)

    def axisParameter(self, commandType, axis, moduleID=None, signed=False):
        value = self.send(TMCL_Command.GAP, commandType, axis, 0, moduleID).value
        if signed:
            return TMC_helpers.toSigned32(value)
        return value

    def setAxisParameter(self, commandType, axis, value, moduleID=None):
        return self.send(TMCL_Command.SAP, commandType, axis, value, moduleID)

    def storeAxisParameter(self, commandType, axis, moduleID=None):
        return self.send(TMCL_Command.STAP, commandType, axis, 0, moduleID)

    def setAndStoreAxisParameter(self, commandType, axis, value, moduleID=None):
        self.send(TMCL_Command.SAP, commandType, axis, value, moduleID)
        self.send(TMCL_Command.STAP, commandType, axis, 0, moduleID)

    def globalParameter(self, commandType, bank, moduleID=None, signed=False):
        value = self.send(TMCL_Command.GGP, commandType, bank, 0, moduleID).value
        if signed:
            return TMC_helpers.toSigned32(value)
        return value

    def setGlobalParameter(self, commandType, bank, value, moduleID=None):
        return self.send(TMCL_Command.SGP, commandType, bank, value, moduleID)

    def storeGlobalParameter(self, commandType, bank, moduleID=None):
        return self.send(TMCL_Command.STGP, commandType, bank, 0, moduleID)

    def setAndStoreGlobalParameter(self, commandType, bank, value, moduleID=None):
        self.send(TMCL_Command.SGP, commandType, bank, value, moduleID)
        self.send(TMCL_Command.STGP, commandType, bank, 0, moduleID)

    def writeMC(self, registerAddress, value, moduleID=None):
        return self.send(TMCL_Command.WRITE_MC, registerAddress, 0, value, moduleID)

    def readMC(self, registerAddress, moduleID=None, signed=False):
        value = self.send(TMCL_Command.READ_MC, registerAddress, 0, 0, moduleID).value
        if signed:
            return TMC_helpers.toSigned32(value)
        return value

    def writeDRV(self, registerAddress, value, moduleID=None):
        return self.send(TMCL_Command.WRITE_DRV, registerAddress, 0, value, moduleID)

    def readDRV(self, registerAddress, moduleID=None, signed=False):
        value = self.send(TMCL_Command.READ_DRV, registerAddress, 0, 0, moduleID).value
        if signed:
            return TMC_helpers.toSigned32(value)
        return value

    def rotate(self, motor, velocity, moduleID=None):
        return self.send(TMCL_Command.ROR, 0, motor, velocity, moduleID)

    def stop(self, motor, moduleID=None):
        return self.send(TMCL_Command.MST, 0, motor, 0, moduleID)

    def move(self, moveType, motor, position, moduleID=None):
        return self.send(TMCL_Command.MVP, moveType, motor, position, moduleID)

    def analogInput(self, x, moduleID=None):
        return self.send(TMCL_Command.GIO, x, 1, 0, moduleID).value

    def digitalInput(self, x, moduleID=None):
        return self.send(TMCL_Command.GIO, x, 0, 0, moduleID).value

    def digitalOutput(self, x, moduleID=None):
        return self.send(TMCL_Command.GIO, x, 2, 0, moduleID).value

    def setDigitalOutput(self, x, moduleID=None):
        self.send(TMCL_Command.SIO, x, 2, 1, moduleID).value

    def clearDigitalOutput(self, x, moduleID=None):
        self.send(TMCL_Command.SIO, x, 2, 0, moduleID).value