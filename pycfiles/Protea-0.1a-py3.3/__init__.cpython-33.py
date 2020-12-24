# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/protea/__init__.py
# Compiled at: 2013-08-24 13:41:10
# Size of source mod 2**32: 11265 bytes
"""Ashly Audio DSP and products Python RS-232 interface library.

This library aims at providing a convenient and simple layer between a python
script and the

Available devices:

    .-------------------------------------.
    | Class name  | Description           |
    |-------------|-----------------------|
    | Protea      | Generic Protea device |
    | P424C       | Protea 4.24C          |
    | Ne2424M     | Protea ne24.24M       |
    '-------------------------------------'

As first parameter for these class, one must pass the name to the serial
interface (that will in turn get opened using the pyserial library), or a 
serial interface object that supports `read`, `write`, `flushInput` and
`flushOutput` methods.
"""
__all__ = [
 'Protea', 'Ne2424M', 'P424C']
from protea.exceptions import SerialInterfaceError, InvalidMessageType, InvalidMessageContent
from time import sleep as _sleep

class Protea(object):
    __doc__ = 'Base class for devices in the Protea family.\n\n    Subclasses must define the _header property as an array of bytes.\n    '
    _baudrate = 38400
    _midi_channel = 1
    _header = None
    _start_byte = 240
    _stop_byte = 247

    def write_message(self, message_type, message_content):
        """
        message_content: bytes() array
        message_type: single byte
        """
        assert self._header, 'Cannot read or write to undefined Protea model!'
        base_message = bytearray()
        base_message.append(self._start_byte)
        base_message += self._header
        base_message.append(message_type)
        message = base_message + message_content
        message.append(self._stop_byte)
        self._serial.flushOutput()
        self._serial.flushInput()
        self._serial.write(message)

    def __init__(self, serial_interface):
        if isinstance(serial_interface, str) or serial_interface is None:
            try:
                import serial
            except ImportError:
                raise SerialInterfaceError('pyserial module was not found and no serial interface was provided.')
            else:
                self._serial = serial.Serial(serial_interface or 0, baudrate=self._baudrate, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE)
        else:
            self._serial = serial_interface
        self._serial.setTimeout(0.5)
        return


class P424C(Protea):
    __doc__ = 'Device class for the Protea 4.24C System Processor unit'
    _baudrate = 9600

    def _force_9600bps(self):
        """This method is required because the 4.24C usually communicates in 31.25kbps,
        but since this is a non-standard speed for RS-232, the machine will switch to
        9600 bps after having received a couple of bytes at that speed.
        """
        self._serial.flushInput()
        self._serial.write(bytes([0] * 6))
        preamble = self._serial.read(10)
        status = preamble == bytes([249] * 10)
        return status

    def __init__(self, serial_interface, midi_channel):
        if not 1 <= midi_channel <= 16:
            raise ValueError('The midi_channel value must be between 1 and 16')
        super(P424C, self).__init__(serial_interface)
        self._midi_channel = midi_channel
        self._force_9600bps()
        self._header = bytearray([0, 1, 42, 3, midi_channel - 1])

    def preset_recall(self, preset_number, muted=False):
        """Recalls a preset on the Protea 4.24C device"""
        if not 1 <= preset_number <= 30:
            raise ValueError('Recalled preset must be between 1 and 31')
        self.write_message(21, bytes([preset_number - 1, 1]))
        response = self._serial.read(10)
        if not muted:
            _sleep(3.5)
            self.write_message(21, bytes([preset_number - 1, 0]))
            response = self._serial.read(10)


class Ne2424M(Protea):
    __doc__ = 'Device class for the Protea ne24.24M matrix processor'
    _header = bytearray([0, 1, 42, 6, 0])

    @staticmethod
    def is_valid_message(message):
        """Checks the validity of a message.

        Messages in the Protea RS-232 protocol start
        with 0xf0 and end with 0xf7.
        """
        return message[0] == 240 and message[(-1)] == 247

    def get_message_length(self, message_type):
        """Depending on message type, this function might
        return a dict instead of an int. If this is the case, then
        the message length is equivalent to:

            returned_length[ message[ message_type_off +1 ] ]

        That is, the byte that is following the message type in the actual
        message will tell us how long the message is supposed to be.
        """
        try:
            length = self.get_message_length.message_lengths[message_type]
        except KeyError:
            raise InvalidMessageType('Not a valid message type: {#x}'.format(message_type))
        else:
            return length

    get_message_length.message_lengths = {0: 10, 
     1: {0: 33,  1: 160,  2: 180},  2: 8, 
     3: 59, 
     4: 8, 
     5: 708, 
     6: 29, 
     7: 10, 
     8: {1: 160,  2: 180},  9: 29, 
     10: 10, 
     11: 11, 
     12: 11, 
     13: 12, 
     14: 17, 
     15: 14, 
     16: 15, 
     17: 13, 
     18: 13, 
     19: 14, 
     20: 15, 
     21: 10, 
     22: 10, 
     23: 9, 
     25: 11, 
     26: 10, 
     66: 9}

    def write_message(self, message_type, message_content):
        """
        message_content: bytes() array
        message_type: single byte
        """
        base_message = bytearray()
        base_message.append(self._start_byte)
        base_message += self._header
        base_message.append(message_type)
        message = base_message + message_content
        message.append(self._stop_byte)
        self._serial.flushOutput()
        self._serial.flushInput()
        self._serial.write(message)

    def get_data_request(self, input_channel=None, output_channel=None):
        """General "data request" Protea function.

        This is used to fetch configuration information for the current preset,
        or information relative to the inputs and outputs, one at a time.

        Input and output are 1-based channel numbers between 1 and 60.

        DATA REQUEST MESSAGE TEMPLATE:

          7: 00     Data request
          8: xx     Data request type (00=config, 01=input, 02=output)
          9: yy     Channel number (00-3b: channel 1-60. 00 for config)
        """
        if input_channel and output_channel:
            raise ValueError('Either an audio input, output, or no parameter at all must be passed to this function')
        else:
            if input_channel:
                assert 0 < input_channel <= 60
                request_type = 1
                channel_number = input_channel - 1
            else:
                if output_channel:
                    assert 0 < output_channel <= 60
                    request_type = 2
                    channel_number = output_channel - 1
                else:
                    request_type = 0
                    channel_number = 0
        message_type = 0
        self.write_message(message_type, bytes([request_type, channel_number]))
        response_length = self.get_message_length(1)[request_type]
        raw_response = self._serial.read(response_length)
        if not self.is_valid_message(raw_response):
            raise InvalidMessageContent('The Protea device sent an unrecognized message! ', raw_response)
        response = {}
        response['message_type'] = raw_response[6]
        response['response_type'] = raw_response[7]
        response['preset_name'] = raw_response[8:28].decode('ascii').rstrip('\x00')
        response['preset_number'] = raw_response[30] + 1
        return response

    def preset_recall(self, preset, muted=False):
        """Recalls a local preset on the ne24.24M device.

        `preset` is an integer between 1 and 31.
        """
        if not 1 <= preset <= 31:
            raise ValueError('Recalled preset must be between 1 and 31')
        self.write_message(7, bytes([preset - 1, 1 if muted else 0]))
        self._serial.read(10)

    def mute_all_outputs(self, mute=True):
        """Mutes all outputs of the ne24.24M"""
        self.write_message(23, bytes([1 if mute else 0]))
        self._serial.read(9)