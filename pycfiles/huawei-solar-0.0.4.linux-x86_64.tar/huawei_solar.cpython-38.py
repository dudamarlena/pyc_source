# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.8/site-packages/huawei_solar/huawei_solar.py
# Compiled at: 2020-04-16 16:28:17
# Size of source mod 2**32: 25803 bytes
"""
Get production and status information from the Huawei Inverter using Modbus over TCP
"""
import asyncio, logging
from collections import namedtuple
from datetime import datetime
import pytz
from pymodbus.client.asynchronous import schedulers
from pymodbus.client.asynchronous.tcp import AsyncModbusTCPClient
from pymodbus.client.sync import ModbusTcpClient
import pymodbus.exceptions as ModbusConnectionException
LOGGER = logging.getLogger(__name__)
RegisterDefinitions = namedtuple('RegisterDefinitions', 'type unit gain register length')
GridCode = namedtuple('GridCode', 'standard country')
Result = namedtuple('Result', 'value unit')
Alarm = namedtuple('Alarm', 'name id level')

class HuaweiSolar:
    __doc__ = 'Interface to the Huawei solar inverter'

    def __init__(self, host, port='502', timeout=5):
        self.client = ModbusTcpClient(host, port=port, timeout=timeout)
        self._time_offset = None

    def get(self, name):
        """get named register from device"""
        reg = REGISTERS[name]
        response = read_register(self.client, reg.register, reg.length)
        if reg.type == 'str':
            result = response.decode('utf-8').strip('\x00')
        else:
            if reg.type == 'u16':
                if reg.unit == 'status_enum':
                    result = DEVICE_STATUS_DEFINITIONS[response.hex()]
                else:
                    if reg.type == 'u16' and reg.unit == 'grid_enum':
                        tmp = int.from_bytes(response, byteorder='big')
                        result = GRID_CODES[tmp]
                    else:
                        if reg.type == 'u32' and reg.unit == 'epoch':
                            tmp = int.from_bytes(response, byteorder='big')
                            if self._time_offset is None:
                                self._time_offset = self.get('time_zone').value
                            tmp2 = datetime.utcfromtimestamp(tmp - 60 * self._time_offset)
                            result = pytz.utc.normalize(pytz.utc.localize(tmp2, is_dst=True))
                        else:
                            if reg.type == 'u16' or reg.type == 'u32':
                                tmp = int.from_bytes(response, byteorder='big')
                                if reg.gain == 1:
                                    result = tmp
                            else:
                                result = tmp / reg.gain
            else:
                if reg.type == 'i16':
                    tmp = int.from_bytes(response, byteorder='big')
                    if tmp & 32768 == 32768:
                        tmp = -((tmp ^ 65535) + 1)
                    if reg.gain == 1:
                        result = tmp
                    else:
                        result = tmp / reg.gain
                else:
                    if reg.type == 'i32':
                        tmp = int.from_bytes(response, byteorder='big')
                        if tmp & 2147483648 == 2147483648:
                            tmp = -((tmp ^ 4294967295) + 1)
                        if reg.gain == 1:
                            result = tmp
                        else:
                            result = tmp / reg.gain
                    else:
                        if reg.type == 'alarm_bitfield16':
                            code = int.from_bytes(response, byteorder='big')
                            result = []
                            alarm_codes = ALARM_CODES[name]
                            for key in alarm_codes:
                                if key & code:
                                    result.append(alarm_codes[key])

                        else:
                            if reg.type == 'state_bitfield16':
                                code = int.from_bytes(response, byteorder='big')
                                result = []
                                for key in STATE_CODES_1:
                                    if key & code:
                                        result.append(STATE_CODES_1[key])

                            else:
                                if reg.type == 'state_opt_bitfield16':
                                    code = int.from_bytes(response, byteorder='big')
                                    result = []
                                    for key in STATE_CODES_2:
                                        bit = key & code
                                        if bit:
                                            result.append(STATE_CODES_2[key][1])
                                        else:
                                            result.append(STATE_CODES_2[key][0])

                                else:
                                    if reg.type == 'state_opt_bitfield32':
                                        code = int.from_bytes(response, byteorder='big')
                                        result = []
                                        for key in STATE_CODES_3:
                                            bit = key & code
                                            if bit:
                                                result.append(STATE_CODES_3[key][1])
                                            else:
                                                result.append(STATE_CODES_3[key][0])

                                    else:
                                        result = int.from_bytes(response, byteorder='big')
        return Result(result, reg.unit)


def read_register(client, register, length):
    """
    Read register from device
    5 tries and then we give up.
    Consistently works after 3 tries if we haven't made requests for a while;
    for sequential requests 1 try is enough from the second request.
    With faster timeout it goes faster, but also fails more than 3 times.
    It seems to only support connections from one device at the same time.
    """
    i = 0
    while i < 5:
        try:
            response = client.read_holding_registers(register, length)
        except ModbusConnectionException as ex:
            try:
                LOGGER.exception('failed to connect to device, is the host correct?')
                raise ConnectionException(ex)
            finally:
                ex = None
                del ex

        else:
            if not response.isError():
                break
            LOGGER.debug('Failed reading register %s time(s)', i)
            i = i + 1

    message = 'could not read register value, is an other device already connected?'
    LOGGER.error(message)
    raise ReadException(message)
    return response.encode()[1:]


class AsyncHuaweiSolar:
    __doc__ = 'Async interface to the Huawei solar inverter'

    def __init__(self, host, port='502', timeout=5, loop=None):
        LOGGER.debug('creating loop and client')
        self.loop, self.client = AsyncModbusTCPClient((schedulers.ASYNC_IO),
          port=port, host=host, loop=loop)
        LOGGER.debug('created loop and client')
        self.timeout = timeout
        self._time_offset = None

    async def get(self, name):
        """get named register from device"""
        reg = REGISTERS[name]
        response = await self.read_register(self.client, reg.register, reg.length)
        if reg.type == 'str':
            result = response.decode('utf-8').strip('\x00')
        else:
            if reg.type == 'u16':
                if reg.unit == 'status_enum':
                    result = DEVICE_STATUS_DEFINITIONS[response.hex()]
                else:
                    if reg.type == 'u16' and reg.unit == 'grid_enum':
                        tmp = int.from_bytes(response, byteorder='big')
                        result = GRID_CODES[tmp]
                    else:
                        if reg.type == 'u32' and reg.unit == 'epoch':
                            tmp = int.from_bytes(response, byteorder='big')
                            if self._time_offset is None:
                                self._time_offset = self.get('time_zone').value
                            tmp2 = datetime.utcfromtimestamp(tmp - 60 * self._time_offset)
                            result = pytz.utc.normalize(pytz.utc.localize(tmp2, is_dst=True))
                        else:
                            if reg.type == 'u16' or reg.type == 'u32':
                                tmp = int.from_bytes(response, byteorder='big')
                                if reg.gain == 1:
                                    result = tmp
                            else:
                                result = tmp / reg.gain
            else:
                if reg.type == 'i16':
                    tmp = int.from_bytes(response, byteorder='big')
                    if tmp & 32768 == 32768:
                        tmp = -((tmp ^ 65535) + 1)
                    if reg.gain == 1:
                        result = tmp
                    else:
                        result = tmp / reg.gain
                else:
                    if reg.type == 'i32':
                        tmp = int.from_bytes(response, byteorder='big')
                        if tmp & 2147483648 == 2147483648:
                            tmp = -((tmp ^ 4294967295) + 1)
                        if reg.gain == 1:
                            result = tmp
                        else:
                            result = tmp / reg.gain
                    else:
                        if reg.type == 'alarm_bitfield16':
                            code = int.from_bytes(response, byteorder='big')
                            result = []
                            alarm_codes = ALARM_CODES[name]
                            for key in alarm_codes:
                                if key & code:
                                    result.append(alarm_codes[key])

                        else:
                            if reg.type == 'state_bitfield16':
                                code = int.from_bytes(response, byteorder='big')
                                result = []
                                for key in STATE_CODES_1:
                                    if key & code:
                                        result.append(STATE_CODES_1[key])

                            else:
                                if reg.type == 'state_opt_bitfield16':
                                    code = int.from_bytes(response, byteorder='big')
                                    result = []
                                    for key in STATE_CODES_2:
                                        bit = key & code
                                        if bit:
                                            result.append(STATE_CODES_2[key][1])
                                        else:
                                            result.append(STATE_CODES_2[key][0])

                                else:
                                    if reg.type == 'state_opt_bitfield32':
                                        code = int.from_bytes(response, byteorder='big')
                                        result = []
                                        for key in STATE_CODES_3:
                                            bit = key & code
                                            if bit:
                                                result.append(STATE_CODES_3[key][1])
                                            else:
                                                result.append(STATE_CODES_3[key][0])

                                    else:
                                        result = int.from_bytes(response, byteorder='big')
        return Result(result, reg.unit)

    async def read_register--- This code section failed: ---

 L. 270         0  LOAD_GLOBAL              range
                2  LOAD_CONST               1
                4  LOAD_CONST               6
                6  CALL_FUNCTION_2       2  ''
                8  GET_ITER         
               10  FOR_ITER            174  'to 174'
               12  STORE_FAST               'i'

 L. 271        14  LOAD_FAST                'client'
               16  LOAD_ATTR                connected
               18  POP_JUMP_IF_TRUE     42  'to 42'

 L. 272        20  LOAD_STR                 'failed to connect to device, is the host correct?'
               22  STORE_FAST               'message'

 L. 273        24  LOAD_GLOBAL              LOGGER
               26  LOAD_METHOD              exception
               28  LOAD_FAST                'message'
               30  CALL_METHOD_1         1  ''
               32  POP_TOP          

 L. 274        34  LOAD_GLOBAL              ConnectionException
               36  LOAD_FAST                'message'
               38  CALL_FUNCTION_1       1  ''
               40  RAISE_VARARGS_1       1  'exception instance'
             42_0  COME_FROM            18  '18'

 L. 275        42  SETUP_FINALLY        98  'to 98'

 L. 276        44  LOAD_GLOBAL              asyncio
               46  LOAD_ATTR                wait_for

 L. 277        48  LOAD_FAST                'client'
               50  LOAD_ATTR                protocol
               52  LOAD_METHOD              read_holding_registers
               54  LOAD_FAST                'register'
               56  LOAD_FAST                'length'
               58  CALL_METHOD_2         2  ''

 L. 278        60  LOAD_FAST                'self'
               62  LOAD_ATTR                timeout

 L. 276        64  LOAD_CONST               ('timeout',)
               66  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               68  GET_AWAITABLE    
               70  LOAD_CONST               None
               72  YIELD_FROM       
               74  STORE_FAST               'response'

 L. 280        76  LOAD_FAST                'response'
               78  LOAD_METHOD              encode
               80  CALL_METHOD_0         0  ''
               82  LOAD_CONST               1
               84  LOAD_CONST               None
               86  BUILD_SLICE_2         2 
               88  BINARY_SUBSCR    
               90  POP_BLOCK        
               92  ROT_TWO          
               94  POP_TOP          
               96  RETURN_VALUE     
             98_0  COME_FROM_FINALLY    42  '42'

 L. 281        98  DUP_TOP          
              100  LOAD_GLOBAL              asyncio
              102  LOAD_ATTR                TimeoutError
              104  COMPARE_OP               exception-match
              106  POP_JUMP_IF_FALSE   130  'to 130'
              108  POP_TOP          
              110  POP_TOP          
              112  POP_TOP          

 L. 282       114  LOAD_GLOBAL              LOGGER
              116  LOAD_METHOD              debug
              118  LOAD_STR                 'Failed reading register %s time(s)'
              120  LOAD_FAST                'i'
              122  CALL_METHOD_2         2  ''
              124  POP_TOP          
              126  POP_EXCEPT       
              128  JUMP_BACK            10  'to 10'
            130_0  COME_FROM           106  '106'

 L. 283       130  DUP_TOP          
              132  LOAD_GLOBAL              ModbusConnectionException
              134  COMPARE_OP               exception-match
              136  POP_JUMP_IF_FALSE   170  'to 170'
              138  POP_TOP          
              140  POP_TOP          
              142  POP_TOP          

 L. 285       144  LOAD_STR                 'could not read register value, is an other device already connected?'

 L. 284       146  STORE_FAST               'message'

 L. 288       148  LOAD_GLOBAL              LOGGER
              150  LOAD_METHOD              error
              152  LOAD_FAST                'message'
              154  CALL_METHOD_1         1  ''
              156  POP_TOP          

 L. 289       158  LOAD_GLOBAL              ReadException
              160  LOAD_FAST                'message'
              162  CALL_FUNCTION_1       1  ''
              164  RAISE_VARARGS_1       1  'exception instance'
              166  POP_EXCEPT       
              168  JUMP_BACK            10  'to 10'
            170_0  COME_FROM           136  '136'
              170  END_FINALLY      
              172  JUMP_BACK            10  'to 10'

 L. 292       174  LOAD_STR                 'could not read register value for unknown reason'
              176  STORE_FAST               'message'

 L. 293       178  LOAD_GLOBAL              LOGGER
              180  LOAD_METHOD              error
              182  LOAD_FAST                'message'
              184  CALL_METHOD_1         1  ''
              186  POP_TOP          

 L. 294       188  LOAD_GLOBAL              ReadException
              190  LOAD_FAST                'message'
              192  CALL_FUNCTION_1       1  ''
              194  RAISE_VARARGS_1       1  'exception instance'

Parse error at or near `ROT_TWO' instruction at offset 92


class ConnectionException(Exception):
    __doc__ = 'Exception connecting to device'


class ReadException(Exception):
    __doc__ = 'Exception reading register from device'


REGISTERS = {'model_name':RegisterDefinitions('str', None, 1, 30000, 15), 
 'serial_number':RegisterDefinitions('str', None, 1, 30015, 10), 
 'model_id':RegisterDefinitions('u16', None, 1, 30070, 1), 
 'nb_pv_strings':RegisterDefinitions('u16', None, 1, 30071, 1), 
 'nb_mpp_tracks':RegisterDefinitions('u16', None, 1, 30072, 1), 
 'rated_power':RegisterDefinitions('u32', 'W', 1, 30073, 2), 
 'P_max':RegisterDefinitions('u32', 'W', 1, 30075, 2), 
 'S_max':RegisterDefinitions('u32', 'VA', 1, 30077, 2), 
 'Q_max_out':RegisterDefinitions('i32', 'VAr', 1, 30079, 2), 
 'Q_max_in':RegisterDefinitions('i32', 'VAr', 1, 30081, 2), 
 'state_1':RegisterDefinitions('state_bitfield16', None, 1, 32000, 1), 
 'state_2':RegisterDefinitions('state_opt_bitfield16', None, 1, 32002, 1), 
 'state_3':RegisterDefinitions('state_opt_bitfield32', None, 1, 32003, 2), 
 'alarm_1':RegisterDefinitions('alarm_bitfield16', None, 1, 32008, 1), 
 'alarm_2':RegisterDefinitions('alarm_bitfield16', None, 1, 32009, 1), 
 'alarm_3':RegisterDefinitions('alarm_bitfield16', None, 1, 32010, 1), 
 'pv_01_voltage':RegisterDefinitions('i16', 'V', 10, 32016, 1), 
 'pv_01_current':RegisterDefinitions('i16', 'A', 100, 32017, 1), 
 'pv_02_voltage':RegisterDefinitions('i16', 'V', 10, 32018, 1), 
 'pv_02_current':RegisterDefinitions('i16', 'A', 100, 32019, 1), 
 'pv_03_voltage':RegisterDefinitions('i16', 'V', 10, 32020, 1), 
 'pv_03_current':RegisterDefinitions('i16', 'A', 100, 32021, 1), 
 'pv_04_voltage':RegisterDefinitions('i16', 'V', 10, 32022, 1), 
 'pv_04_current':RegisterDefinitions('i16', 'A', 100, 32023, 1), 
 'pv_05_voltage':RegisterDefinitions('i16', 'V', 10, 32024, 1), 
 'pv_05_current':RegisterDefinitions('i16', 'A', 100, 32025, 1), 
 'pv_06_voltage':RegisterDefinitions('i16', 'V', 10, 32026, 1), 
 'pv_06_current':RegisterDefinitions('i16', 'A', 100, 32027, 1), 
 'pv_07_voltage':RegisterDefinitions('i16', 'V', 10, 32028, 1), 
 'pv_07_current':RegisterDefinitions('i16', 'A', 100, 32029, 1), 
 'pv_08_voltage':RegisterDefinitions('i16', 'V', 10, 32030, 1), 
 'pv_08_current':RegisterDefinitions('i16', 'A', 100, 32031, 1), 
 'pv_09_voltage':RegisterDefinitions('i16', 'V', 10, 32032, 1), 
 'pv_09_current':RegisterDefinitions('i16', 'A', 100, 32033, 1), 
 'pv_10_voltage':RegisterDefinitions('i16', 'V', 10, 32034, 1), 
 'pv_10_current':RegisterDefinitions('i16', 'A', 100, 32035, 1), 
 'pv_11_voltage':RegisterDefinitions('i16', 'V', 10, 32036, 1), 
 'pv_11_current':RegisterDefinitions('i16', 'A', 100, 32037, 1), 
 'pv_12_voltage':RegisterDefinitions('i16', 'V', 10, 32038, 1), 
 'pv_12_current':RegisterDefinitions('i16', 'A', 100, 32039, 1), 
 'pv_13_voltage':RegisterDefinitions('i16', 'V', 10, 32040, 1), 
 'pv_13_current':RegisterDefinitions('i16', 'A', 100, 32041, 1), 
 'pv_14_voltage':RegisterDefinitions('i16', 'V', 10, 32042, 1), 
 'pv_14_current':RegisterDefinitions('i16', 'A', 100, 32043, 1), 
 'pv_15_voltage':RegisterDefinitions('i16', 'V', 10, 32044, 1), 
 'pv_15_current':RegisterDefinitions('i16', 'A', 100, 32045, 1), 
 'pv_16_voltage':RegisterDefinitions('i16', 'V', 10, 32046, 1), 
 'pv_16_current':RegisterDefinitions('i16', 'A', 100, 32047, 1), 
 'pv_17_voltage':RegisterDefinitions('i16', 'V', 10, 32048, 1), 
 'pv_17_current':RegisterDefinitions('i16', 'A', 100, 32049, 1), 
 'pv_18_voltage':RegisterDefinitions('i16', 'V', 10, 32050, 1), 
 'pv_18_current':RegisterDefinitions('i16', 'A', 100, 32051, 1), 
 'pv_19_voltage':RegisterDefinitions('i16', 'V', 10, 32052, 1), 
 'pv_19_current':RegisterDefinitions('i16', 'A', 100, 32053, 1), 
 'pv_20_voltage':RegisterDefinitions('i16', 'V', 10, 32054, 1), 
 'pv_20_current':RegisterDefinitions('i16', 'A', 100, 32055, 1), 
 'pv_21_voltage':RegisterDefinitions('i16', 'V', 10, 32056, 1), 
 'pv_21_current':RegisterDefinitions('i16', 'A', 100, 32057, 1), 
 'pv_22_voltage':RegisterDefinitions('i16', 'V', 10, 32058, 1), 
 'pv_22_current':RegisterDefinitions('i16', 'A', 100, 32059, 1), 
 'pv_23_voltage':RegisterDefinitions('i16', 'V', 10, 32060, 1), 
 'pv_23_current':RegisterDefinitions('i16', 'A', 100, 32061, 1), 
 'pv_24_voltage':RegisterDefinitions('i16', 'V', 10, 32062, 1), 
 'pv_24_current':RegisterDefinitions('i16', 'A', 100, 32063, 1), 
 'input_power':RegisterDefinitions('i32', 'W', 1, 32064, 2), 
 'grid_voltage':RegisterDefinitions('u16', 'V', 10, 32066, 1), 
 'line_voltage_A_B':RegisterDefinitions('u16', 'V', 10, 32066, 1), 
 'line_voltage_B_C':RegisterDefinitions('u16', 'V', 10, 32067, 1), 
 'line_voltage_C_A':RegisterDefinitions('u16', 'V', 10, 32068, 1), 
 'phase_A_voltage':RegisterDefinitions('u16', 'V', 10, 32069, 1), 
 'phase_B_voltage':RegisterDefinitions('u16', 'V', 10, 32070, 1), 
 'phase_C_voltage':RegisterDefinitions('u16', 'V', 10, 32071, 1), 
 'grid_current':RegisterDefinitions('i32', 'A', 1000, 32072, 2), 
 'phase_A_current':RegisterDefinitions('i32', 'A', 1000, 32072, 2), 
 'phase_B_current':RegisterDefinitions('i32', 'A', 1000, 32074, 2), 
 'phase_C_current':RegisterDefinitions('i32', 'A', 1000, 32076, 2), 
 'day_active_power_peak':RegisterDefinitions('i32', 'W', 1, 32078, 2), 
 'active_power':RegisterDefinitions('i32', 'W', 1, 32080, 2), 
 'reactive_power':RegisterDefinitions('i32', 'VA', 1, 32082, 2), 
 'power_factor':RegisterDefinitions('i16', None, 1000, 32084, 1), 
 'grid_frequency':RegisterDefinitions('u16', 'Hz', 100, 32085, 1), 
 'efficiency':RegisterDefinitions('u16', '%', 100, 32086, 1), 
 'internal_temperature':RegisterDefinitions('i16', '°C', 10, 32087, 1), 
 'insulation_resistance':RegisterDefinitions('u16', 'MOhm', 100, 32088, 1), 
 'device_status':RegisterDefinitions('u16', 'status_enum', 1, 32089, 1), 
 'fault_code':RegisterDefinitions('u16', None, 1, 32090, 1), 
 'startup_time':RegisterDefinitions('u32', 'epoch', 1, 32091, 2), 
 'shutdown_time':RegisterDefinitions('u32', 'epoch', 1, 32093, 2), 
 'accumulated_yield_energy':RegisterDefinitions('u32', 'kWh', 100, 32106, 2), 
 'power_meter_active_power':RegisterDefinitions('i32', 'W', 1, 37113, 2), 
 'daily_yield_energy':RegisterDefinitions('u32', 'kWh', 100, 32114, 2), 
 'nb_optimizers':RegisterDefinitions('u16', None, 1, 37200, 1), 
 'nb_online_optimizers':RegisterDefinitions('u16', None, 1, 37201, 1), 
 'system_time':RegisterDefinitions('u32', 'epoch', 1, 40000, 2), 
 'grid_code':RegisterDefinitions('u16', 'grid_enum', 1, 42000, 1), 
 'time_zone':RegisterDefinitions('i16', 'min', 1, 43006, 1)}
DEVICE_STATUS_DEFINITIONS = {'0000':'Standby: initializing', 
 '0001':'Standby: detecting insulation resistance', 
 '0002':'Standby: detecting irradiation', 
 '0003':'Standby: grid detecting', 
 '0100':'Starting', 
 '0200':'On-grid', 
 '0201':'Grid Connection: power limited', 
 '0202':'Grid Connection: self-derating', 
 '0300':'Shutdown: fault', 
 '0301':'Shutdown: command', 
 '0302':'Shutdown: OVGR', 
 '0303':'Shutdown: communication disconnected', 
 '0304':'Shutdown: power limited', 
 '0305':'Shutdown: manual startup required', 
 '0306':'Shutdown: DC switches disconnected', 
 '0307':'Shutdown: rapid cutoff', 
 '0308':'Shutdown: input underpowered', 
 '0401':'Grid scheduling: cosphi-P curve', 
 '0402':'Grid scheduling: Q-U curve', 
 '0403':'Grid scheduling: PF-U curve', 
 '0404':'Grid scheduling: dry contact', 
 '0405':'Grid scheduling: Q-P curve', 
 '0500':'Spot-check ready', 
 '0501':'Spot-checking', 
 '0600':'Inspecting', 
 '0700':'AFCI self check', 
 '0800':'I-V scanning', 
 '0900':'DC input detection', 
 '0a00':'Running: off-grid charging', 
 'a000':'Standby: no irradiation'}
GRID_CODES = {0:GridCode('VDE-AR-N-4105', 'Germany'), 
 1:GridCode('NB/T 32004', 'China'), 
 2:GridCode('UTE C 15-712-1(A)', 'France'), 
 3:GridCode('UTE C 15-712-1(B)', 'France'), 
 4:GridCode('UTE C 15-712-1(C)', 'France'), 
 5:GridCode('VDE 0126-1-1-BU', 'Bulgary'), 
 6:GridCode('VDE 0126-1-1-GR(A)', 'Greece'), 
 7:GridCode('VDE 0126-1-1-GR(B)', 'Greece'), 
 8:GridCode('BDEW-MV', 'Germany'), 
 9:GridCode('G59-England', 'UK'), 
 10:GridCode('G59-Scotland', 'UK'), 
 11:GridCode('G83-England', 'UK'), 
 12:GridCode('G83-Scotland', 'UK'), 
 13:GridCode('CEI0-21', 'Italy'), 
 14:GridCode('EN50438-CZ', 'Czech Republic'), 
 15:GridCode('RD1699/661', 'Spain'), 
 16:GridCode('RD1699/661-MV480', 'Spain'), 
 17:GridCode('EN50438-NL', 'Netherlands'), 
 18:GridCode('C10/11', 'Belgium'), 
 19:GridCode('AS4777', 'Australia'), 
 20:GridCode('IEC61727', 'General'), 
 21:GridCode('Custom (50 Hz)', 'Custom'), 
 22:GridCode('Custom (60 Hz)', 'Custom'), 
 23:GridCode('CEI0-16', 'Italy'), 
 24:GridCode('CHINA-MV480', 'China'), 
 25:GridCode('CHINA-MV', 'China'), 
 26:GridCode('TAI-PEA', 'Thailand'), 
 27:GridCode('TAI-MEA', 'Thailand'), 
 28:GridCode('BDEW-MV480', 'Germany'), 
 29:GridCode('Custom MV480 (50 Hz)', 'Custom'), 
 30:GridCode('Custom MV480 (60 Hz)', 'Custom'), 
 31:GridCode('G59-England-MV480', 'UK'), 
 32:GridCode('IEC61727-MV480', 'General'), 
 33:GridCode('UTE C 15-712-1-MV480', 'France'), 
 34:GridCode('TAI-PEA-MV480', 'Thailand'), 
 35:GridCode('TAI-MEA-MV480', 'Thailand'), 
 36:GridCode('EN50438-DK-MV480', 'Denmark'), 
 37:GridCode('Japan standard (50 Hz)', 'Japan'), 
 38:GridCode('Japan standard (60 Hz)', 'Japan'), 
 39:GridCode('EN50438-TR-MV480', 'Turkey'), 
 40:GridCode('EN50438-TR', 'Turkey'), 
 41:GridCode('C11/C10-MV480', 'Belgium'), 
 42:GridCode('Philippines', 'Philippines'), 
 43:GridCode('Philippines-MV480', 'Philippines'), 
 44:GridCode('AS4777-MV480', 'Australia'), 
 45:GridCode('NRS-097-2-1', 'South Africa'), 
 46:GridCode('NRS-097-2-1-MV480', 'South Africa'), 
 47:GridCode('KOREA', 'South Korea'), 
 48:GridCode('IEEE 1547-MV480', 'USA'), 
 49:GridCode('IEC61727-60Hz', 'General'), 
 50:GridCode('IEC61727-60Hz-MV480', 'General')}
STATE_CODES_1 = {1:'standby', 
 2:'grid-connected', 
 4:'grid-connected normally', 
 8:'grid connection with derating due to power rationing', 
 16:'grid connection with derating due to internalcausesof the solar inverter', 
 32:'normal stop', 
 64:'stop due to faults', 
 128:'stop due to power rationing', 
 256:'shutdown', 
 512:'spot check'}
STATE_CODES_2 = {1:('locked', 'unlocked'), 
 2:('PV disconnected', 'PV connected'), 
 4:('no DSP data collection', 'DSP data collection')}
STATE_CODES_3 = {1:('on-grid', 'off-grid'), 
 2:('off-grid switch disabled', 'off-grid switch enabled')}
ALARM_CODES_1 = {1:Alarm('High String Input Voltage', 2001, 'Major'), 
 2:Alarm('DC Arc Fault', 2002, 'Major'), 
 4:Alarm('String Reverse Connection', 2011, 'Major'), 
 8:Alarm('String Current Backfeed', 2012, 'Warning'), 
 16:Alarm('Abnormal String Power', 2013, 'Warning'), 
 32:Alarm('AFCI Self-Check Fail', 2021, 'Major'), 
 64:Alarm('Phase Wire Short-Circuited to PE', 2031, 'Major'), 
 128:Alarm('Grid Loss', 2032, 'Major'), 
 256:Alarm('Grid Undervoltage', 2033, 'Major'), 
 512:Alarm('Grid Overvoltage', 2034, 'Major'), 
 1024:Alarm('Grid Volt. Imbalance', 2035, 'Major'), 
 2048:Alarm('Grid Overfrequency', 2036, 'Major'), 
 4096:Alarm('Grid Underfrequency', 2037, 'Major'), 
 8192:Alarm('Unstable Grid Frequency', 2038, 'Major'), 
 16384:Alarm('Output Overcurrent', 2039, 'Major'), 
 32768:Alarm('Output DC Component Overhigh', 2040, 'Major')}
ALARM_CODES_2 = {1:Alarm('Abnormal Residual Current', 2051, 'Major'), 
 2:Alarm('Abnormal Grounding', 2061, 'Major'), 
 4:Alarm('Low Insulation Resistance', 2062, 'Major'), 
 8:Alarm('Overtemperature', 2063, 'Minor'), 
 16:Alarm('Device Fault', 2064, 'Major'), 
 32:Alarm('Upgrade Failed or Version Mismatch', 2065, 'Minor'), 
 64:Alarm('License Expired', 2066, 'Warning'), 
 128:Alarm('Faulty Monitoring Unit', 61440, 'Minor'), 
 256:Alarm('Faulty Power Collector', 2067, 'Major'), 
 512:Alarm('Battery abnormal', 2068, 'Minor'), 
 1024:Alarm('Active Islanding', 2070, 'Major'), 
 2048:Alarm('Passive Islanding', 2071, 'Major'), 
 4096:Alarm('Transient AC Overvoltage', 2072, 'Major'), 
 8192:Alarm('Peripheral port short circuit', 2075, 'Warning'), 
 16384:Alarm('Churn output overload', 2077, 'Major'), 
 32768:Alarm('Abnormal PV module configuration', 2080, 'Major')}
ALARM_CODES_3 = {1:Alarm('Optimizer fault', 2081, 'Warning'), 
 2:Alarm('Built-in PID operation abnormal', 2085, 'Minor'), 
 4:Alarm('High input string voltage to ground', 2014, 'Major'), 
 8:Alarm('External Fan Abnormal', 2086, 'Major'), 
 16:Alarm('Battery Reverse Connection', 2069, 'Major'), 
 32:Alarm('On-grid/Off-grid controller abnormal', 2082, 'Major'), 
 64:Alarm('PV String Loss', 2015, 'Warning'), 
 128:Alarm('Internal Fan Abnormal', 2087, 'Major'), 
 256:Alarm('DC Protection Unit Abnormal', 2088, 'Major')}
ALARM_CODES = {'alarm_1':ALARM_CODES_1, 
 'alarm_2':ALARM_CODES_2, 
 'alarm_3':ALARM_CODES_3}