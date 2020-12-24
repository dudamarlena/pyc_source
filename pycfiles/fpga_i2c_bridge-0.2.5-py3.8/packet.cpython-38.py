# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/fpga_i2c_bridge/net/packet.py
# Compiled at: 2020-04-09 04:36:35
# Size of source mod 2**32: 11365 bytes
"""Gateway to FPGA smart bridge protocol, containing command and response representations."""
from __future__ import annotations
from collections import namedtuple
from typing import Union
from fpga_i2c_bridge.net.error import I2CUnknownOpcodeException, I2CNoSuchDeviceException, I2CException, I2CNoDataException, I2CRecvCRCFailureException, I2CSendCRCFailureException
from fpga_i2c_bridge.util.crc import crc16
OP_APPLIANCE_GET_STATE = 0
OP_APPLIANCE_GET_TYPE = 1
OP_SENSOR_GET_TYPE = 2
OP_APPLIANCE_SET_STATE = 16
OP_FPGA_GET_STATUS = 32
OP_FPGA_RESET = 47
OP_POLL = 48
OP_REPEAT_LAST_MESSAGE = 64
POLL_TYPE_INPUT = 0
POLL_TYPE_UPDATE = 1
STATUS_OK = 240
STATUS_ERROR = 241
STATUS_NO_DATA = 242
ERR_UNKNOWN_CMD = 16
ERR_NO_SUCH_DEVICE = 32
ERR_CRC_FAILURE = 48
ERR_UNKNOWN_FAILURE = 255
_EXCEPTIONS = {ERR_UNKNOWN_CMD: lambda x: I2CUnknownOpcodeException(*x), 
 ERR_NO_SUCH_DEVICE: lambda x: I2CNoSuchDeviceException(*x), 
 ERR_CRC_FAILURE: lambda x: I2CSendCRCFailureException(), 
 ERR_UNKNOWN_FAILURE: lambda x: I2CException('FPGA reported unknown failure')}
FPGAStatus = namedtuple('FPGAStatus', 'version num_outputs num_inputs')

class I2CCommand:
    __doc__ = 'Base class for I2C commands.'

    def __init__(self, opcode: 'int'):
        self.opcode = opcode

    def parameters(self) -> 'tuple':
        """
        Returns the raw parameter data as an iterable of ints. When translating a command object into bytes, these
        values will be used as the command parameters, following the command's opcode.
        """
        return ()

    def handle_reply(self, reply: 'bytes') -> 'I2CResponse':
        """
        This method handles a response from the FPGA.
        Because the response does not indicate its type, each command dictates the kind of response it expects.
        Should the response contain a status code other than OK, this will throw the appropriate exception.
        :param reply: FPGA response data
        :return: Response object
        """
        if crc16(reply) > 0:
            raise I2CRecvCRCFailureException()
        if reply[0] == STATUS_ERROR:
            try:
                raise _EXCEPTIONS[reply[1]](reply[2:])
            except KeyError:
                raise I2CException('Unknown error of type %02x reported' % reply[1])

        if reply[0] == STATUS_NO_DATA:
            raise I2CNoDataException()
        return self.construct_reply(reply[1:])

    def construct_reply(self, reply: 'bytes') -> 'I2CResponse':
        """
        Constructs a response object from the FPGA response bytes and returns it.
        By default, this returns an empty response.
        :param reply: FPGA response data
        :return: Response object
        """
        return I2CResponse()

    def ship(self) -> 'bytes':
        """
        Translates itself to its byte representation.
        :return: Command as bytes
        """
        msg = bytes((self.opcode,) + self.parameters())
        crc = crc16(msg)
        return msg + int.to_bytes(crc, 2, 'big')


class I2CSetApplianceStateCommand(I2CCommand):
    __doc__ = '\n    Represents a Set Appliance State command.\n    This command does not expect a response.\n    '

    def __init__(self, device_id, new_state):
        super(I2CSetApplianceStateCommand, self).__init__(OP_APPLIANCE_SET_STATE)
        self.device_id = device_id
        self.new_state = new_state

    def parameters(self) -> 'tuple':
        """
        Defines the Set Appliance State command's parameters.
        :return: Tuple of appliance ID and new 3-byte raw state value, MSB first.
        """
        return (
         self.device_id, self.new_state >> 16 & 255, self.new_state >> 8 & 255, self.new_state & 255)


class I2CGetApplianceStateCommand(I2CCommand):
    __doc__ = '\n    Represents a Get Appliance State command.\n    This command expects a response containing the device ID and state.\n    '

    def __init__(self, device_id):
        super(I2CGetApplianceStateCommand, self).__init__(OP_APPLIANCE_GET_STATE)
        self.device_id = device_id

    def parameters(self) -> 'tuple':
        """
        Defines the Get Appliance State command's parameters.
        :return: Tuple of device ID
        """
        return (
         self.device_id,)

    def construct_reply(self, reply: 'bytes') -> 'I2CApplianceStateResponse':
        """
        Constructs the Get Appliance State response.
        :param reply: FPGA response data
        :return: Appliance state response, containing device ID and three-byte state, MSB first
        """
        return I2CApplianceStateResponse(device_id=(reply[0]), device_state=((reply[1] << 16) + (reply[2] << 8) + reply[3]))


class I2CGetApplianceTypeCommand(I2CCommand):
    __doc__ = '\n    Represents a Get Appliance Type command.\n    This command expects a response containing the device ID and its type.\n    '

    def __init__(self, device_id):
        super(I2CGetApplianceTypeCommand, self).__init__(OP_APPLIANCE_GET_TYPE)
        self.device_id = device_id

    def parameters(self) -> 'tuple':
        """
        Defines the Get Appliance Type command's parameters.
        :return: Tuple of appliance ID
        """
        return (
         self.device_id,)

    def construct_reply(self, reply: 'bytes') -> 'I2CApplianceTypeResponse':
        """
        Constructs the Get Appliance Type response.
        :param reply: FPGA response data
        :return: Appliance type response, containing device ID and type
        """
        return I2CApplianceTypeResponse(device_id=(reply[0]), device_type=(reply[1]))


class I2CGetSensorTypeCommand(I2CCommand):
    __doc__ = '\n    Represents a Get Sensor Type command.\n    This command expects a response containing the sensor device ID and its type.\n    '

    def __init__(self, sensor_id):
        super(I2CGetSensorTypeCommand, self).__init__(OP_SENSOR_GET_TYPE)
        self.sensor_id = sensor_id

    def parameters(self) -> 'tuple':
        """
        Defines the Get Sensor Type command's parameters.
        :return: Tuple of sensor device ID
        """
        return (
         self.sensor_id,)

    def construct_reply(self, reply: 'bytes') -> 'I2CSensorTypeResponse':
        """
        Constructs the Get Sensor Type response.
        :param reply: FPGA response data
        :return: Sensor Type reply, containing sensor device ID and type
        """
        return I2CSensorTypeResponse(sensor_id=(reply[0]), sensor_type=(reply[1]))


class I2CGetFPGAStatusCommand(I2CCommand):
    __doc__ = '\n    Represents a Get FPGA Status Command.\n    Expects a response containing two-byte FPGA version, MSB first, as well as highest IDs of appliances and sensors,\n    respectively.\n    '

    def __init__(self):
        super(I2CGetFPGAStatusCommand, self).__init__(OP_FPGA_GET_STATUS)

    def construct_reply(self, reply: 'bytes') -> 'I2CFPGAStatusResponse':
        """
        Constructs the Get FPGA Status Command response.
        :param reply: FPGA response data
        :return: Get FPGA Status response, containing two-byte FPGA version, MSB first, as well as highest IDs of
        appliances and sensors.
        """
        return I2CFPGAStatusResponse(version=((reply[0] << 8) + reply[1]), num_appliances=(reply[2]),
          num_sensors=(reply[3]))


class I2CResetFPGACommand(I2CCommand):
    __doc__ = '\n    Represents a Reset FPGA command.\n    This command does not expect a response.\n    '

    def __init__(self):
        super(I2CResetFPGACommand, self).__init__(OP_FPGA_RESET)


class I2CPollCommand(I2CCommand):
    __doc__ = '\n    Represents a Poll command.\n    This command expects a response containing either a State Update or Input event.\n    '

    def __init__(self):
        super(I2CPollCommand, self).__init__(OP_POLL)

    def construct_reply(self, reply: 'bytes') -> 'Union[I2CApplianceStateResponse, I2CInputEventResponse]':
        """
        Constructs the Poll response.
        Should the response contain an unknown event type, a I2CException will be thrown.
        :param reply: FPGA response data
        :return: Either one of Appliance State or Input Event response
        """
        if reply[0] == POLL_TYPE_UPDATE:
            return I2CApplianceStateResponse(device_id=(reply[1]), device_state=((reply[2] << 16) + (reply[3] << 8) + reply[4]))
        if reply[0] == POLL_TYPE_INPUT:
            return I2CInputEventResponse(sensor_id=(reply[1]), sensor_data=((reply[2] << 16) + (reply[3] << 8) + reply[4]))
        raise I2CException('Unknown event type %02x received' % reply[0])


class I2CRepeatLastMessageCommand(I2CCommand):
    __doc__ = '\n    Represents a Repeat Last Message command.\n    The expected response depends on the command that was sent prior.\n    '

    def __init__(self, last_command):
        super(I2CRepeatLastMessageCommand, self).__init__(OP_REPEAT_LAST_MESSAGE)
        self.last_command = last_command

    def construct_reply(self, reply: 'bytes') -> 'I2CResponse':
        """
        Constructs a Repeat Last Message response.
        :param reply: FPGA response data
        :return: Response to the command that was sent prior to this one.
        """
        return self.last_command.construct_reply(reply)


class I2CResponse:
    __doc__ = 'Base class for FPGA responses.'


class I2CFPGAStatusResponse(I2CResponse):
    __doc__ = '\n    Represents a FPGA Status response.\n    '

    def __init__(self, version, num_appliances, num_sensors):
        super(I2CFPGAStatusResponse, self).__init__()
        self.version = version
        self.num_appliances = num_appliances
        self.num_sensors = num_sensors


class I2CApplianceStateResponse(I2CResponse):
    __doc__ = '\n    Represents an Appliance State response.\n    '

    def __init__(self, device_id, device_state):
        super(I2CApplianceStateResponse, self).__init__()
        self.device_id = device_id
        self.device_state = device_state


class I2CApplianceTypeResponse(I2CResponse):
    __doc__ = '\n    Represents an Appliance Type response.\n    '

    def __init__(self, device_id, device_type):
        super(I2CApplianceTypeResponse, self).__init__()
        self.device_id = device_id
        self.device_type = device_type


class I2CSensorTypeResponse(I2CResponse):
    __doc__ = '\n    Represents a Sensor Type response.\n    '

    def __init__(self, sensor_id, sensor_type):
        super(I2CSensorTypeResponse, self).__init__()
        self.sensor_id = sensor_id
        self.sensor_type = sensor_type


class I2CInputEventResponse(I2CResponse):
    __doc__ = '\n    Represents an Input Event response.\n    '

    def __init__(self, sensor_id, sensor_data):
        super(I2CInputEventResponse, self).__init__()
        self.sensor_id = sensor_id
        self.sensor_data = sensor_data