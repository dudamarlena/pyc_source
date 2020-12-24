# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/fpga_i2c_bridge/i2c.py
# Compiled at: 2020-04-09 04:36:35
# Size of source mod 2**32: 7090 bytes
"""Representations for the I2C bus."""
from abc import ABC
from typing import List, Union
from fpga_i2c_bridge.net.error import I2CNoDataException, I2CRecvCRCFailureException, I2CSendCRCFailureException, I2CException, I2CCommunicationError
from fpga_i2c_bridge.net.packet import I2CGetApplianceStateCommand, I2CGetApplianceTypeCommand, I2CSetApplianceStateCommand, I2CGetFPGAStatusCommand, I2CResetFPGACommand, I2CPollCommand, FPGAStatus, I2CResponse, I2CRepeatLastMessageCommand, I2CGetSensorTypeCommand, I2CCommand, I2CApplianceStateResponse, I2CApplianceTypeResponse, I2CSensorTypeResponse, I2CFPGAStatusResponse, I2CInputEventResponse
from fpga_i2c_bridge.util import Logger

class I2CBus(ABC):
    __doc__ = '\n    Abstract class for representing an I2C bbus.\n    '

    def __init__(self, max_retries: int=10, *args, **kwargs):
        self.logger = Logger.get_logger(self)
        self.max_retries = max_retries

    def raw_write(self, request: bytes) -> None:
        """
        Writes the specified byte sequence onto the bus.
        :param request: Bytes to write
        """
        raise NotImplementedError()

    def raw_read(self, request: bytes) -> bytes:
        """
        Writes the specified byte sequence onto the bus, then reads the raw response. This will not perform CRC
        checksum verification on the received data.
        :param request: Bytes to write
        :return: Response bytes
        """
        raise NotImplementedError()

    def cmd_write(self, command: I2CCommand) -> None:
        """
        Writes the specified command onto the bus.
        :param command: Command to write
        """
        self.raw_write(command.ship())

    def cmd_read--- This code section failed: ---

 L.  55         0  LOAD_CONST               0
                2  STORE_FAST               'attempt'

 L.  56         4  LOAD_FAST                'command'
                6  STORE_FAST               'orig_command'

 L.  57         8  LOAD_FAST                'attempt'
               10  LOAD_FAST                'self'
               12  LOAD_ATTR                max_retries
               14  COMPARE_OP               <
               16  POP_JUMP_IF_FALSE   162  'to 162'

 L.  58        18  SETUP_FINALLY        54  'to 54'

 L.  59        20  LOAD_FAST                'attempt'
               22  LOAD_CONST               1
               24  INPLACE_ADD      
               26  STORE_FAST               'attempt'

 L.  60        28  LOAD_FAST                'self'
               30  LOAD_METHOD              raw_read
               32  LOAD_FAST                'command'
               34  LOAD_METHOD              ship
               36  CALL_METHOD_0         0  ''
               38  CALL_METHOD_1         1  ''
               40  STORE_FAST               'reply'

 L.  61        42  LOAD_FAST                'command'
               44  LOAD_METHOD              handle_reply
               46  LOAD_FAST                'reply'
               48  CALL_METHOD_1         1  ''
               50  POP_BLOCK        
               52  RETURN_VALUE     
             54_0  COME_FROM_FINALLY    18  '18'

 L.  62        54  DUP_TOP          
               56  LOAD_GLOBAL              I2CRecvCRCFailureException
               58  COMPARE_OP               exception-match
               60  POP_JUMP_IF_FALSE   108  'to 108'
               62  POP_TOP          
               64  POP_TOP          
               66  POP_TOP          

 L.  63        68  LOAD_FAST                'self'
               70  LOAD_ATTR                logger
               72  LOAD_METHOD              info
               74  LOAD_STR                 'CRC failure in message from FPGA, requesting re-send (Attempt '
               76  LOAD_FAST                'attempt'
               78  FORMAT_VALUE          0  ''
               80  LOAD_STR                 '/'
               82  LOAD_FAST                'self'
               84  LOAD_ATTR                max_retries
               86  FORMAT_VALUE          0  ''
               88  LOAD_STR                 ')'
               90  BUILD_STRING_5        5 
               92  CALL_METHOD_1         1  ''
               94  POP_TOP          

 L.  65        96  LOAD_GLOBAL              I2CRepeatLastMessageCommand
               98  LOAD_FAST                'orig_command'
              100  CALL_FUNCTION_1       1  ''
              102  STORE_FAST               'command'
              104  POP_EXCEPT       
              106  JUMP_BACK             8  'to 8'
            108_0  COME_FROM            60  '60'

 L.  66       108  DUP_TOP          
              110  LOAD_GLOBAL              I2CSendCRCFailureException
              112  COMPARE_OP               exception-match
              114  POP_JUMP_IF_FALSE   158  'to 158'
              116  POP_TOP          
              118  POP_TOP          
              120  POP_TOP          

 L.  67       122  LOAD_FAST                'self'
              124  LOAD_ATTR                logger
              126  LOAD_METHOD              info
              128  LOAD_STR                 'Got CRC error from FPGA, re-sending '
              130  LOAD_FAST                'attempt'
              132  FORMAT_VALUE          0  ''
              134  LOAD_STR                 '/'
              136  LOAD_FAST                'self'
              138  LOAD_ATTR                max_retries
              140  FORMAT_VALUE          0  ''
              142  LOAD_STR                 ')'
              144  BUILD_STRING_5        5 
              146  CALL_METHOD_1         1  ''
              148  POP_TOP          

 L.  68       150  LOAD_FAST                'orig_command'
              152  STORE_FAST               'command'
              154  POP_EXCEPT       
              156  JUMP_BACK             8  'to 8'
            158_0  COME_FROM           114  '114'
              158  END_FINALLY      
              160  JUMP_BACK             8  'to 8'
            162_0  COME_FROM            16  '16'

 L.  70       162  LOAD_GLOBAL              I2CCommunicationError
              164  CALL_FUNCTION_0       0  ''
              166  RAISE_VARARGS_1       1  'exception instance'

Parse error at or near `POP_TOP' instruction at offset 64

    def get_appliance_state(self, device_id: int) -> I2CApplianceStateResponse:
        """
        Retrieves the state of the appliance with the supplied ID.
        :param device_id: ID of appliance
        :return: Appliance state response
        """
        return self.cmd_read(I2CGetApplianceStateCommand(device_id))

    def get_appliance_type(self, device_id: int) -> I2CApplianceTypeResponse:
        """
        Retrieves the type of the appliance with the supplied ID.
        :param device_id: ID of appliance
        :return: Appliance type response
        """
        return self.cmd_read(I2CGetApplianceTypeCommand(device_id))

    def get_sensor_type(self, sensor_id: int) -> I2CSensorTypeResponse:
        """
        Retrieves the type of the sensor with the supplied ID.
        :param sensor_id: ID of sensor
        :return: Sensor type response
        """
        return self.cmd_read(I2CGetSensorTypeCommand(sensor_id))

    def set_appliance_state(self, device_id: int, new_state: int) -> None:
        """
        Requests to set the state of the appliance with the specified ID to the specified raw state.
        :param device_id: ID of appliance
        :param new_state: New raw state
        """
        self.cmd_read(I2CSetApplianceStateCommand(device_id, new_state))

    def get_fpga_status(self) -> I2CFPGAStatusResponse:
        """
        Retrieves the status of the FPGA bridge.
        :return: FPGA Status response
        """
        return self.cmd_read(I2CGetFPGAStatusCommand())

    def reset_fpga(self) -> None:
        """Resets the FPGA."""
        self.cmd_write(I2CResetFPGACommand())

    def poll(self) -> List[Union[(I2CApplianceStateResponse, I2CInputEventResponse)]]:
        """
        Polls for new State Update and Input events.
        :return: List of event responses for poll request
        """
        out = []
        while True:
            try:
                out.append(self.cmd_read(I2CPollCommand()))
            except I2CNoDataException:
                break

        return out


class I2CBusReal(I2CBus):
    __doc__ = "Implementation of the I2C bus that uses the hardware's I2C interface through the smbus2 module."

    def __init__(self, bus, addr, *args, **kwargs):
        (super(I2CBusReal, self).__init__)(*args, **kwargs)
        self.bus = bus
        self.addr = addr

    def raw_write(self, request: bytes) -> None:
        """
        Writes the specified byte sequence onto the bus.
        Throws an I2CException should the connection fail.
        :param request: Bytes to write
        """
        from smbus2 import SMBusWrapper, i2c_msg
        with SMBusWrapper(self.bus) as (bus):
            cmd = i2c_msg.write(self.addr, request)
            try:
                self.logger.debug('>> %s' % ' '.join(('%02x' % byte for byte in request)))
                bus.i2c_rdwr(cmd)
            except IOError:
                raise I2CException('IO error in I2C communication')

    def raw_read--- This code section failed: ---

 L. 160         0  LOAD_CONST               0
                2  LOAD_CONST               ('SMBusWrapper', 'i2c_msg')
                4  IMPORT_NAME              smbus2
                6  IMPORT_FROM              SMBusWrapper
                8  STORE_FAST               'SMBusWrapper'
               10  IMPORT_FROM              i2c_msg
               12  STORE_FAST               'i2c_msg'
               14  POP_TOP          

 L. 161        16  LOAD_FAST                'SMBusWrapper'
               18  LOAD_FAST                'self'
               20  LOAD_ATTR                bus
               22  CALL_FUNCTION_1       1  ''
               24  SETUP_WITH          220  'to 220'
               26  STORE_FAST               'bus'

 L. 162        28  LOAD_FAST                'i2c_msg'
               30  LOAD_METHOD              write
               32  LOAD_FAST                'self'
               34  LOAD_ATTR                addr
               36  LOAD_FAST                'request'
               38  CALL_METHOD_2         2  ''
               40  STORE_FAST               'request_cmd'

 L. 163        42  LOAD_FAST                'i2c_msg'
               44  LOAD_METHOD              read
               46  LOAD_FAST                'self'
               48  LOAD_ATTR                addr
               50  LOAD_CONST               8
               52  CALL_METHOD_2         2  ''
               54  STORE_FAST               'response_cmd'

 L. 165        56  LOAD_FAST                'self'
               58  LOAD_ATTR                logger
               60  LOAD_METHOD              debug
               62  LOAD_STR                 '>> %s'
               64  LOAD_STR                 ' '
               66  LOAD_METHOD              join
               68  LOAD_GENEXPR             '<code_object <genexpr>>'
               70  LOAD_STR                 'I2CBusReal.raw_read.<locals>.<genexpr>'
               72  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               74  LOAD_FAST                'request'
               76  GET_ITER         
               78  CALL_FUNCTION_1       1  ''
               80  CALL_METHOD_1         1  ''
               82  BINARY_MODULO    
               84  CALL_METHOD_1         1  ''
               86  POP_TOP          

 L. 167        88  SETUP_FINALLY       188  'to 188'

 L. 168        90  LOAD_FAST                'bus'
               92  LOAD_METHOD              i2c_rdwr
               94  LOAD_FAST                'request_cmd'
               96  CALL_METHOD_1         1  ''
               98  POP_TOP          

 L. 169       100  LOAD_FAST                'bus'
              102  LOAD_METHOD              i2c_rdwr
              104  LOAD_FAST                'response_cmd'
              106  CALL_METHOD_1         1  ''
              108  POP_TOP          

 L. 171       110  LOAD_CONST               b''
              112  STORE_FAST               'response'

 L. 172       114  LOAD_FAST                'response_cmd'
              116  GET_ITER         
              118  FOR_ITER            138  'to 138'
              120  STORE_FAST               'byte'

 L. 173       122  LOAD_FAST                'response'
              124  LOAD_GLOBAL              bytes
              126  LOAD_FAST                'byte'
              128  BUILD_TUPLE_1         1 
              130  CALL_FUNCTION_1       1  ''
              132  INPLACE_ADD      
              134  STORE_FAST               'response'
              136  JUMP_BACK           118  'to 118'

 L. 175       138  LOAD_FAST                'self'
              140  LOAD_ATTR                logger
              142  LOAD_METHOD              debug
              144  LOAD_STR                 '<< %s'
              146  LOAD_STR                 ' '
              148  LOAD_METHOD              join
              150  LOAD_GENEXPR             '<code_object <genexpr>>'
              152  LOAD_STR                 'I2CBusReal.raw_read.<locals>.<genexpr>'
              154  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              156  LOAD_FAST                'response'
              158  GET_ITER         
              160  CALL_FUNCTION_1       1  ''
              162  CALL_METHOD_1         1  ''
              164  BINARY_MODULO    
              166  CALL_METHOD_1         1  ''
              168  POP_TOP          

 L. 177       170  LOAD_FAST                'response'
              172  POP_BLOCK        
              174  POP_BLOCK        
              176  ROT_TWO          
              178  BEGIN_FINALLY    
              180  WITH_CLEANUP_START
              182  WITH_CLEANUP_FINISH
              184  POP_FINALLY           0  ''
              186  RETURN_VALUE     
            188_0  COME_FROM_FINALLY    88  '88'

 L. 179       188  DUP_TOP          
              190  LOAD_GLOBAL              IOError
              192  COMPARE_OP               exception-match
              194  POP_JUMP_IF_FALSE   214  'to 214'
              196  POP_TOP          
              198  POP_TOP          
              200  POP_TOP          

 L. 180       202  LOAD_GLOBAL              I2CException
              204  LOAD_STR                 'IO error in I2C communication'
              206  CALL_FUNCTION_1       1  ''
              208  RAISE_VARARGS_1       1  'exception instance'
              210  POP_EXCEPT       
              212  JUMP_FORWARD        216  'to 216'
            214_0  COME_FROM           194  '194'
              214  END_FINALLY      
            216_0  COME_FROM           212  '212'
              216  POP_BLOCK        
              218  BEGIN_FINALLY    
            220_0  COME_FROM_WITH       24  '24'
              220  WITH_CLEANUP_START
              222  WITH_CLEANUP_FINISH
              224  END_FINALLY      

Parse error at or near `POP_BLOCK' instruction at offset 174