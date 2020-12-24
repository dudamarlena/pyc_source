# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/fpga_i2c_bridge/i2c_dummy.py
# Compiled at: 2020-04-15 04:30:41
# Size of source mod 2**32: 7800 bytes
"""A dummy implementation of the I2C bus that simulates a real bridge."""
import threading
from collections import deque
from random import random
from time import sleep
from typing import List, Optional
from fpga_i2c_bridge.appliance import I2CShutter
from fpga_i2c_bridge.i2c import I2CBus
from fpga_i2c_bridge.net.packet import OP_APPLIANCE_GET_STATE, STATUS_OK, OP_APPLIANCE_GET_TYPE, OP_APPLIANCE_SET_STATE, OP_FPGA_GET_STATUS, OP_FPGA_RESET, STATUS_ERROR, ERR_NO_SUCH_DEVICE, ERR_UNKNOWN_CMD, OP_POLL, STATUS_NO_DATA, POLL_TYPE_UPDATE, OP_REPEAT_LAST_MESSAGE, ERR_CRC_FAILURE, OP_SENSOR_GET_TYPE
from fpga_i2c_bridge.util import Logger
from fpga_i2c_bridge.util.crc import crc16

def split_state(state: int):
    return (state >> 24, (state >> 16) % 256, state % 256)


class I2CDummyDevice:

    def __init__(self, i2c, device_type, device_id):
        self.i2c = i2c
        self.type = device_type
        self.device_id = device_id
        self.state = 0

    def set_state(self, state: bytes):
        self.state = (state[0] << 16) + (state[1] << 8) + state[2]

    def update(self):
        pass


class I2CDummySwitch(I2CDummyDevice):

    def __init__(self, *args, **kwargs):
        (super(I2CDummySwitch, self).__init__)(args, device_type=1, **kwargs)


class I2CDummyDimmer(I2CDummyDevice):

    def __init__(self, *args, **kwargs):
        (super(I2CDummyDimmer, self).__init__)(args, device_type=2, **kwargs)


class I2CDummyRGB(I2CDummyDevice):

    def __init__(self, *args, **kwargs):
        (super(I2CDummyRGB, self).__init__)(args, device_type=3, **kwargs)


class I2CDummyShutter(I2CDummyDevice):

    def __init__(self, *args, **kwargs):
        (super(I2CDummyShutter, self).__init__)(args, device_type=4, **kwargs)
        self.timer = 0

    def set_state(self, state):
        super().set_state(state)
        encoded = I2CShutter.State(self.state)
        if encoded == I2CShutter.State.UP_ONCE or encoded == I2CShutter.State.DOWN_ONCE:
            self.timer = 10
        else:
            if encoded == I2CShutter.State.UP_FULL or encoded == I2CShutter.State.DOWN_FULL:
                self.timer = 50
            else:
                self.timer = 0

    def update(self):
        if self.timer > 0:
            self.timer -= 1
            if self.timer == 0:
                self.i2c.queue_update(self.device_id, I2CShutter.State.IDLE.value)


_DUMMY_DEVICE_TYPES = {1:I2CDummySwitch, 
 2:I2CDummyDimmer, 
 3:I2CDummyRGB, 
 4:I2CDummyShutter}

class I2CDummy(I2CBus):

    def __init__(self, appliance_types, sensor_types=None, error_ratio=0.0, *args, **kwargs):
        (super(I2CDummy, self).__init__)(*args, **kwargs)
        self.error_ratio = error_ratio
        self.last_message = b''
        self._appliances = {}
        for dev_id, dev_type in enumerate(appliance_types):
            try:
                dev_obj = _DUMMY_DEVICE_TYPES[dev_type](i2c=self, device_id=dev_id)
            except KeyError:
                self.logger.error(f"No device with type {dev_type}, replacing with a Switch")
                dev_obj = _DUMMY_DEVICE_TYPES[1](i2c=self, device_id=dev_id)
            else:
                self._appliances[dev_id] = dev_obj
        else:
            self._sensors = sensor_types or []
            self._updates = deque()
            self._update_thread = threading.Thread(target=(self._device_update_thread), daemon=True)
            self._update_thread.start()

    def _dummy_response(self, *r_bytes) -> bytes:
        out = b''
        for i in range(6):
            out += b'\x00' if i >= len(r_bytes) else bytes((r_bytes[i],))
        else:
            out += int.to_bytes(crc16(out), 2, 'big')
            self.last_message = out
            if self.error_ratio > 0:
                out = self._glitch(out)
            return out

    def _glitch(self, data: bytes) -> bytes:
        if self.error_ratio == 0:
            return data
        out = b''
        for i in range(len(data)):
            byte = data[i]
            for n in range(8):
                if random() < self.error_ratio:
                    byte = byte ^ 1 << n
                out += bytes((byte,))
            else:
                return out

    def _reset(self):
        for dev in self._appliances.values():
            dev.set_state(b'\x00\x00\x00')

    def _has_device(self, device_id):
        return device_id in self._appliances.keys()

    def _dummy_read--- This code section failed: ---

 L. 140         0  LOAD_GLOBAL              crc16
                2  LOAD_FAST                'request'
                4  CALL_FUNCTION_1       1  ''
                6  LOAD_CONST               0
                8  COMPARE_OP               >
               10  POP_JUMP_IF_FALSE    66  'to 66'

 L. 141        12  LOAD_FAST                'self'
               14  LOAD_ATTR                logger
               16  LOAD_METHOD              debug
               18  LOAD_STR                 'Req: %s CRC: %d'
               20  LOAD_GLOBAL              bytes
               22  LOAD_METHOD              hex
               24  LOAD_FAST                'request'
               26  CALL_METHOD_1         1  ''
               28  LOAD_GLOBAL              crc16
               30  LOAD_FAST                'request'
               32  CALL_FUNCTION_1       1  ''
               34  BUILD_TUPLE_2         2 
               36  BINARY_MODULO    
               38  CALL_METHOD_1         1  ''
               40  POP_TOP          

 L. 142        42  LOAD_FAST                'self'
               44  LOAD_ATTR                logger
               46  LOAD_METHOD              info
               48  LOAD_STR                 'CRC failure in message from bridge, requesting re-send'
               50  CALL_METHOD_1         1  ''
               52  POP_TOP          

 L. 143        54  LOAD_FAST                'self'
               56  LOAD_METHOD              _dummy_response
               58  LOAD_GLOBAL              STATUS_ERROR
               60  LOAD_GLOBAL              ERR_CRC_FAILURE
               62  CALL_METHOD_2         2  ''
               64  RETURN_VALUE     
             66_0  COME_FROM            10  '10'

 L. 145        66  LOAD_FAST                'request'
               68  LOAD_CONST               0
               70  BINARY_SUBSCR    
               72  STORE_FAST               'opcode'

 L. 147        74  LOAD_FAST                'opcode'
               76  LOAD_GLOBAL              OP_APPLIANCE_GET_STATE
               78  COMPARE_OP               ==
               80  POP_JUMP_IF_FALSE   148  'to 148'

 L. 148        82  LOAD_FAST                'request'
               84  LOAD_CONST               1
               86  BINARY_SUBSCR    
               88  STORE_FAST               'device_id'

 L. 149        90  LOAD_FAST                'self'
               92  LOAD_METHOD              _has_device
               94  LOAD_FAST                'device_id'
               96  CALL_METHOD_1         1  ''
               98  POP_JUMP_IF_FALSE   130  'to 130'

 L. 150       100  LOAD_FAST                'self'
              102  LOAD_ATTR                _dummy_response
              104  LOAD_GLOBAL              STATUS_OK
              106  LOAD_FAST                'device_id'
              108  BUILD_TUPLE_2         2 
              110  LOAD_GLOBAL              split_state
              112  LOAD_FAST                'self'
              114  LOAD_ATTR                _appliances
              116  LOAD_FAST                'device_id'
              118  BINARY_SUBSCR    
              120  LOAD_ATTR                state
              122  CALL_FUNCTION_1       1  ''
              124  BUILD_TUPLE_UNPACK_WITH_CALL_2     2 
              126  CALL_FUNCTION_EX      0  'positional arguments only'
              128  RETURN_VALUE     
            130_0  COME_FROM            98  '98'

 L. 152       130  LOAD_FAST                'self'
              132  LOAD_METHOD              _dummy_response
              134  LOAD_GLOBAL              STATUS_ERROR
              136  LOAD_GLOBAL              ERR_NO_SUCH_DEVICE
              138  LOAD_FAST                'device_id'
              140  CALL_METHOD_3         3  ''
              142  RETURN_VALUE     
          144_146  JUMP_FORWARD        528  'to 528'
            148_0  COME_FROM            80  '80'

 L. 154       148  LOAD_FAST                'opcode'
              150  LOAD_GLOBAL              OP_APPLIANCE_GET_TYPE
              152  COMPARE_OP               ==
              154  POP_JUMP_IF_FALSE   214  'to 214'

 L. 155       156  LOAD_FAST                'request'
              158  LOAD_CONST               1
              160  BINARY_SUBSCR    
              162  STORE_FAST               'device_id'

 L. 156       164  LOAD_FAST                'self'
              166  LOAD_METHOD              _has_device
              168  LOAD_FAST                'device_id'
              170  CALL_METHOD_1         1  ''
              172  POP_JUMP_IF_FALSE   196  'to 196'

 L. 157       174  LOAD_FAST                'self'
              176  LOAD_METHOD              _dummy_response
              178  LOAD_GLOBAL              STATUS_OK
              180  LOAD_FAST                'device_id'
              182  LOAD_FAST                'self'
              184  LOAD_ATTR                _appliances
              186  LOAD_FAST                'device_id'
              188  BINARY_SUBSCR    
              190  LOAD_ATTR                type
              192  CALL_METHOD_3         3  ''
              194  RETURN_VALUE     
            196_0  COME_FROM           172  '172'

 L. 159       196  LOAD_FAST                'self'
              198  LOAD_METHOD              _dummy_response
              200  LOAD_GLOBAL              STATUS_ERROR
              202  LOAD_GLOBAL              ERR_NO_SUCH_DEVICE
              204  LOAD_FAST                'device_id'
              206  CALL_METHOD_3         3  ''
              208  RETURN_VALUE     
          210_212  JUMP_FORWARD        528  'to 528'
            214_0  COME_FROM           154  '154'

 L. 161       214  LOAD_FAST                'opcode'
              216  LOAD_GLOBAL              OP_SENSOR_GET_TYPE
              218  COMPARE_OP               ==
          220_222  POP_JUMP_IF_FALSE   298  'to 298'

 L. 162       224  LOAD_FAST                'request'
              226  LOAD_CONST               1
              228  BINARY_SUBSCR    
              230  STORE_FAST               'input_id'

 L. 163       232  SETUP_FINALLY       260  'to 260'

 L. 164       234  LOAD_FAST                'self'
              236  LOAD_ATTR                _sensors
              238  LOAD_FAST                'input_id'
              240  BINARY_SUBSCR    
              242  STORE_FAST               'input_type'

 L. 165       244  LOAD_FAST                'self'
              246  LOAD_METHOD              _dummy_response
              248  LOAD_GLOBAL              STATUS_OK
              250  LOAD_FAST                'input_id'
              252  LOAD_FAST                'input_type'
              254  CALL_METHOD_3         3  ''
              256  POP_BLOCK        
              258  RETURN_VALUE     
            260_0  COME_FROM_FINALLY   232  '232'

 L. 166       260  DUP_TOP          
              262  LOAD_GLOBAL              IndexError
              264  COMPARE_OP               exception-match
          266_268  POP_JUMP_IF_FALSE   294  'to 294'
              270  POP_TOP          
              272  POP_TOP          
              274  POP_TOP          

 L. 167       276  LOAD_FAST                'self'
              278  LOAD_METHOD              _dummy_response
              280  LOAD_GLOBAL              STATUS_ERROR
              282  LOAD_GLOBAL              ERR_NO_SUCH_DEVICE
              284  LOAD_FAST                'input_id'
              286  CALL_METHOD_3         3  ''
              288  ROT_FOUR         
              290  POP_EXCEPT       
              292  RETURN_VALUE     
            294_0  COME_FROM           266  '266'
              294  END_FINALLY      
              296  JUMP_FORWARD        528  'to 528'
            298_0  COME_FROM           220  '220'

 L. 169       298  LOAD_FAST                'opcode'
              300  LOAD_GLOBAL              OP_APPLIANCE_SET_STATE
              302  COMPARE_OP               ==
          304_306  POP_JUMP_IF_FALSE   378  'to 378'

 L. 170       308  LOAD_FAST                'request'
              310  LOAD_CONST               1
              312  BINARY_SUBSCR    
              314  STORE_FAST               'device_id'

 L. 171       316  LOAD_FAST                'self'
              318  LOAD_METHOD              _has_device
              320  LOAD_FAST                'device_id'
              322  CALL_METHOD_1         1  ''
          324_326  POP_JUMP_IF_FALSE   362  'to 362'

 L. 172       328  LOAD_FAST                'self'
              330  LOAD_ATTR                _appliances
              332  LOAD_FAST                'device_id'
              334  BINARY_SUBSCR    
              336  LOAD_METHOD              set_state
              338  LOAD_FAST                'request'
              340  LOAD_CONST               2
              342  LOAD_CONST               5
              344  BUILD_SLICE_2         2 
              346  BINARY_SUBSCR    
              348  CALL_METHOD_1         1  ''
              350  POP_TOP          

 L. 173       352  LOAD_FAST                'self'
              354  LOAD_METHOD              _dummy_response
              356  LOAD_GLOBAL              STATUS_OK
              358  CALL_METHOD_1         1  ''
              360  RETURN_VALUE     
            362_0  COME_FROM           324  '324'

 L. 175       362  LOAD_FAST                'self'
              364  LOAD_METHOD              _dummy_response
              366  LOAD_GLOBAL              STATUS_ERROR
              368  LOAD_GLOBAL              ERR_NO_SUCH_DEVICE
              370  LOAD_FAST                'device_id'
              372  CALL_METHOD_3         3  ''
              374  RETURN_VALUE     
              376  JUMP_FORWARD        528  'to 528'
            378_0  COME_FROM           304  '304'

 L. 177       378  LOAD_FAST                'opcode'
              380  LOAD_GLOBAL              OP_FPGA_GET_STATUS
              382  COMPARE_OP               ==
          384_386  POP_JUMP_IF_FALSE   418  'to 418'

 L. 178       388  LOAD_FAST                'self'
              390  LOAD_METHOD              _dummy_response
              392  LOAD_GLOBAL              STATUS_OK
              394  LOAD_CONST               222
              396  LOAD_CONST               173
              398  LOAD_GLOBAL              len
              400  LOAD_FAST                'self'
              402  LOAD_ATTR                _appliances
              404  CALL_FUNCTION_1       1  ''
              406  LOAD_GLOBAL              len
              408  LOAD_FAST                'self'
              410  LOAD_ATTR                _sensors
              412  CALL_FUNCTION_1       1  ''
              414  CALL_METHOD_5         5  ''
              416  RETURN_VALUE     
            418_0  COME_FROM           384  '384'

 L. 180       418  LOAD_FAST                'opcode'
              420  LOAD_GLOBAL              OP_POLL
              422  COMPARE_OP               ==
          424_426  POP_JUMP_IF_FALSE   464  'to 464'

 L. 181       428  LOAD_GLOBAL              len
              430  LOAD_FAST                'self'
              432  LOAD_ATTR                _updates
              434  CALL_FUNCTION_1       1  ''
              436  LOAD_CONST               0
              438  COMPARE_OP               >
          440_442  POP_JUMP_IF_FALSE   454  'to 454'

 L. 182       444  LOAD_FAST                'self'
              446  LOAD_ATTR                _updates
              448  LOAD_METHOD              popleft
              450  CALL_METHOD_0         0  ''
              452  RETURN_VALUE     
            454_0  COME_FROM           440  '440'

 L. 184       454  LOAD_FAST                'self'
              456  LOAD_METHOD              _dummy_response
              458  LOAD_GLOBAL              STATUS_NO_DATA
              460  CALL_METHOD_1         1  ''
              462  RETURN_VALUE     
            464_0  COME_FROM           424  '424'

 L. 186       464  LOAD_FAST                'opcode'
              466  LOAD_GLOBAL              OP_REPEAT_LAST_MESSAGE
              468  COMPARE_OP               ==
          470_472  POP_JUMP_IF_FALSE   486  'to 486'

 L. 187       474  LOAD_FAST                'self'
              476  LOAD_METHOD              _glitch
              478  LOAD_FAST                'self'
              480  LOAD_ATTR                last_message
              482  CALL_METHOD_1         1  ''
              484  RETURN_VALUE     
            486_0  COME_FROM           470  '470'

 L. 189       486  LOAD_FAST                'opcode'
              488  LOAD_GLOBAL              OP_FPGA_RESET
              490  COMPARE_OP               ==
          492_494  POP_JUMP_IF_FALSE   514  'to 514'

 L. 190       496  LOAD_FAST                'self'
              498  LOAD_METHOD              _reset
              500  CALL_METHOD_0         0  ''
              502  POP_TOP          

 L. 191       504  LOAD_FAST                'self'
              506  LOAD_METHOD              _dummy_response
              508  LOAD_GLOBAL              STATUS_OK
              510  CALL_METHOD_1         1  ''
              512  RETURN_VALUE     
            514_0  COME_FROM           492  '492'

 L. 194       514  LOAD_FAST                'self'
              516  LOAD_METHOD              _dummy_response
              518  LOAD_GLOBAL              STATUS_ERROR
              520  LOAD_GLOBAL              ERR_UNKNOWN_CMD
              522  LOAD_FAST                'opcode'
              524  CALL_METHOD_3         3  ''
              526  RETURN_VALUE     
            528_0  COME_FROM           376  '376'
            528_1  COME_FROM           296  '296'
            528_2  COME_FROM           210  '210'
            528_3  COME_FROM           144  '144'

Parse error at or near `POP_TOP' instruction at offset 272

    def queue_update(self, device_id: int, state: int):
        self.logger.debug('Received device state update: Device %d, State %06x' % (device_id, state))
        self._updates.append((self._dummy_response)(STATUS_OK, POLL_TYPE_UPDATE, device_id, *split_state(state)))

    def _device_update_thread(self):
        self.logger.info('Starting dummy device update thread')
        try:
            while True:
                for device in self._appliances.values():
                    device.update()
                else:
                    sleep(0.1)

        except (KeyboardInterrupt, SystemExit):
            self.logger.info('Closing dummy device update thread')

    def raw_write(self, request: bytes) -> None:
        self._dummy_read(request)
        self.logger.debug('>> %s' % ' '.join(('%02x' % byte for byte in request)))

    def raw_read(self, request: bytes) -> bytes:
        self.logger.debug('>> %s' % ' '.join(('%02x' % byte for byte in request)))
        response = self._dummy_read(self._glitch(request))
        self.logger.debug('<< %s' % ' '.join(('%02x' % byte for byte in response)))
        return response