# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/fpga_i2c_bridge/appliance.py
# Compiled at: 2020-04-09 08:22:24
# Size of source mod 2**32: 10105 bytes
"""FPGA appliance representations."""
from enum import Enum
from typing import Any, Tuple, Optional
from fpga_i2c_bridge.util import Logger

class InvalidStateError(BaseException):
    __doc__ = 'Exception that gets thrown when an invalid state value has been supplied for an appliance.'

    def __init__(self, device, state):
        super(InvalidStateError, self).__init__('%s is not a valid state for device %s' % (state, device))


class UnknownDeviceTypeError(BaseException):
    __doc__ = 'Exception that gets thrown when a device of an unknown type is attempted to be created.'

    def __init__(self, device_type):
        super(UnknownDeviceTypeError, self).__init__(f"Attempted to instantiate device of unknown type {device_type}")


class I2CApplianceType(Enum):
    __doc__ = 'Enumeration for all appliance types.'
    BINARY = 1
    DIMMER = 2
    RGB = 3
    SHUTTER = 4


class I2CAppliance:
    __doc__ = 'Abstract class for representing an appliance.'

    def __init__(self, bridge: 'I2CBridge', device_id: int, device_type: I2CApplianceType, default_state: Optional[Any]=None):
        """The bridge this appliance belongs to."""
        self.bridge = bridge
        self.device_id = device_id
        self.device_type = device_type
        self.state = default_state
        self.logger = Logger.get_logger(self)
        self._update_handlers = {}

    @staticmethod
    def create--- This code section failed: ---

 L.  59         0  SETUP_FINALLY        20  'to 20'

 L.  60         2  LOAD_GLOBAL              _DEVICE_CLASSES
                4  LOAD_FAST                'device_type'
                6  BINARY_SUBSCR    
                8  LOAD_FAST                'bridge'
               10  LOAD_FAST                'device_id'
               12  LOAD_CONST               ('bridge', 'device_id')
               14  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               16  POP_BLOCK        
               18  RETURN_VALUE     
             20_0  COME_FROM_FINALLY     0  '0'

 L.  61        20  DUP_TOP          
               22  LOAD_GLOBAL              KeyError
               24  COMPARE_OP               exception-match
               26  POP_JUMP_IF_FALSE    46  'to 46'
               28  POP_TOP          
               30  POP_TOP          
               32  POP_TOP          

 L.  62        34  LOAD_GLOBAL              UnknownDeviceTypeError
               36  LOAD_FAST                'device_type'
               38  CALL_FUNCTION_1       1  ''
               40  RAISE_VARARGS_1       1  'exception instance'
               42  POP_EXCEPT       
               44  JUMP_FORWARD         48  'to 48'
             46_0  COME_FROM            26  '26'
               46  END_FINALLY      
             48_0  COME_FROM            44  '44'

Parse error at or near `POP_TOP' instruction at offset 30

    def _encode_state(self, state: Any) -> int:
        """
        Translates the given state value to its raw 24-bit form.
        :param state: State to translate
        :return: Raw 24-bit state
        """
        raise NotImplementedError

    def _decode_state(self, raw_state: int) -> Any:
        """
        Translates the given raw 24-bit state into a more sensible type.
        :param raw_state: Raw 24-bit state
        :return: Interpreted state value
        """
        raise NotImplementedError

    def set_state(self, new_state: Any) -> None:
        """
        Requests to set the state of this appliance to the given value, which needs to be a valid state value in the
        context of this device.
        :param new_state: New state value to set
        """
        encoded_state = self._encode_state(new_state)
        self.logger.info('Set state to %s (0x%06x)' % (new_state, encoded_state))
        if self.bridge.send_state(self.device_id, encoded_state):
            self.state = new_state

    def update_state(self, new_state: int) -> None:
        """
        Updates its own state. This is done after receiving a State Update event, and will call all state update
        handler callbacks.
        :param new_state: New raw 24-bit state value
        """
        self.state = self._decode_state(new_state)
        self.logger.debug('State update: %s (Raw: %06x)' % (self.state, new_state))
        self._call_update_handlers()

    def register_update_handler(self):
        """
        Decorator that registers the following function as a callback that will be called when this appliance updates
        its own state through a State Update event.
        The function must not take any parameters.
        :return: Decorator
        """

        def decorator(function):

            def wrapper(*args, **kwargs):
                return function(*args, **kwargs)

            self._update_handlers[function.__name__] = wrapper

        return decorator

    def _call_update_handlers(self):
        for func in self._update_handlers.values():
            func()

    def __str__(self):
        return 'ID %d' % self.device_id


class I2CGenericBinary(I2CAppliance):
    __doc__ = 'Represents a Generic Binary device.'

    def __init__(self, bridge, device_id):
        super(I2CGenericBinary, self).__init__(bridge=bridge, device_id=device_id, device_type=(I2CApplianceType.BINARY), default_state=False)

    def _encode_state(self, state: bool) -> int:
        """
        Translates the given state to its raw 24-bit equivalent. This returns 0 for False and 1 for True.
        :param state: Generic Binary state to translate
        :return: 0 for False, or 1 for True
        """
        return int(state)

    def _decode_state(self, raw_state: int) -> bool:
        """
        Translates the given raw 24-bit state to a Boolean value. This returns False for 0, and True otherwise.
        :param raw_state: Raw 24-bit state value
        :return: False for 0, True otherwise
        """
        return bool(raw_state)

    def turn_on(self) -> None:
        """
        Turns on the Generic Binary appliance.
        """
        self.set_state(True)

    def turn_off(self) -> None:
        """
        Turns off the Generic Binary appliance.
        """
        self.set_state(False)

    def toggle(self) -> None:
        """
        Toggles the state of the Generic Binary appliance.
        """
        self.set_state(not self.state)

    def __str__(self):
        return 'Switch (%s)' % super().__str__()


class I2CDimmer(I2CAppliance):
    __doc__ = 'Represents a Dimmer appliance.'

    def __init__(self, bridge, device_id):
        super(I2CDimmer, self).__init__(bridge=bridge, device_id=device_id, device_type=(I2CApplianceType.DIMMER), default_state=0.0)

    def _encode_state(self, state: float) -> int:
        try:
            if 0 <= state <= 1:
                return round(state * 255)
            raise TypeError
        except TypeError:
            raise InvalidStateError(self, state)

    def _decode_state(self, raw_state: int) -> float:
        return raw_state % 256 / 255

    def set_brightness(self, brightness: float) -> None:
        """
        Sets the brightness of this Dimmer. It is expressed through a float value between 0 and 1 inclusive, with
        0 being off, and 1 being the maximum possible brightness.
        :param brightness: Brightness value as a float between 0 and 1 inclusive
        """
        self.set_state(brightness)

    def __str__(self):
        return 'Dimmer (%s)' % super().__str__()


class I2CRGBDimmer(I2CAppliance):
    __doc__ = 'Represents a RGB Dimmer appliance.'

    def __init__(self, bridge, device_id):
        super(I2CRGBDimmer, self).__init__(bridge=bridge, device_id=device_id, device_type=(I2CApplianceType.RGB), default_state=(0,
                                                                                                                                  0,
                                                                                                                                  0))

    def _encode_state(self, state: Tuple[(float, float, float)]) -> int:
        try:
            if 0 <= state[0] <= 1:
                if 0 <= state[1] <= 1:
                    if 0 <= state[2] <= 1:
                        return (int(255 * state[0]) << 16) + (int(255 * state[1]) << 8) + int(state[2] * 255)
            raise TypeError
        except TypeError:
            raise InvalidStateError(self, state)

    def _decode_state(self, raw_state: int) -> Tuple[(float, float, float)]:
        return ((raw_state >> 16) / 255, (raw_state >> 8) % 256 / 255, raw_state % 256 / 255)

    def set_color(self, color: Tuple[(float, float, float)]) -> None:
        """
        Sets the color of this RGB Dimmer. It is expressed as a RGB color triplet, with values for each color ranging
        from 0 to 1 inclusive.
        :param color: Tuple of red, green and blue colors, each ranging from 0 to 1 inclusive
        """
        self.set_state(color)

    def __str__(self):
        return 'RGB Dimmer (%s)' % super().__str__()


class I2CShutter(I2CAppliance):
    __doc__ = 'Represents a Shutter appliance.'

    class State(Enum):
        __doc__ = "Enumeration for the Shutter's possible state values."
        IDLE = 0
        UP_ONCE = 1
        UP_FULL = 2
        DOWN_ONCE = 3
        DOWN_FULL = 4

    def __init__(self, bridge, device_id):
        super(I2CShutter, self).__init__(bridge=bridge, device_id=device_id, device_type=(I2CApplianceType.SHUTTER), default_state=(I2CShutter.State.IDLE))

    def _encode_state--- This code section failed: ---

 L. 248         0  SETUP_FINALLY        10  'to 10'

 L. 249         2  LOAD_FAST                'state'
                4  LOAD_ATTR                value
                6  POP_BLOCK        
                8  RETURN_VALUE     
             10_0  COME_FROM_FINALLY     0  '0'

 L. 250        10  DUP_TOP          
               12  LOAD_GLOBAL              ValueError
               14  COMPARE_OP               exception-match
               16  POP_JUMP_IF_FALSE    38  'to 38'
               18  POP_TOP          
               20  POP_TOP          
               22  POP_TOP          

 L. 251        24  LOAD_GLOBAL              InvalidStateError
               26  LOAD_FAST                'self'
               28  LOAD_FAST                'state'
               30  CALL_FUNCTION_2       2  ''
               32  RAISE_VARARGS_1       1  'exception instance'
               34  POP_EXCEPT       
               36  JUMP_FORWARD         40  'to 40'
             38_0  COME_FROM            16  '16'
               38  END_FINALLY      
             40_0  COME_FROM            36  '36'

Parse error at or near `POP_TOP' instruction at offset 20

    def _decode_state--- This code section failed: ---

 L. 254         0  SETUP_FINALLY        14  'to 14'

 L. 255         2  LOAD_FAST                'self'
                4  LOAD_METHOD              State
                6  LOAD_FAST                'raw_state'
                8  CALL_METHOD_1         1  ''
               10  POP_BLOCK        
               12  RETURN_VALUE     
             14_0  COME_FROM_FINALLY     0  '0'

 L. 256        14  DUP_TOP          
               16  LOAD_GLOBAL              ValueError
               18  COMPARE_OP               exception-match
               20  POP_JUMP_IF_FALSE    42  'to 42'
               22  POP_TOP          
               24  POP_TOP          
               26  POP_TOP          

 L. 257        28  LOAD_GLOBAL              InvalidStateError
               30  LOAD_FAST                'self'
               32  LOAD_FAST                'raw_state'
               34  CALL_FUNCTION_2       2  ''
               36  RAISE_VARARGS_1       1  'exception instance'
               38  POP_EXCEPT       
               40  JUMP_FORWARD         44  'to 44'
             42_0  COME_FROM            20  '20'
               42  END_FINALLY      
             44_0  COME_FROM            40  '40'

Parse error at or near `POP_TOP' instruction at offset 24

    def stop(self) -> None:
        """Stops this Shutter from moving."""
        self.set_state(self.State.IDLE)

    def move_up(self) -> None:
        """Moves this Shutter up for one movement cycle."""
        self.set_state(self.State.UP_ONCE)

    def move_up_full(self) -> None:
        """Moves this Shutter up fully."""
        self.set_state(self.State.UP_FULL)

    def move_down(self) -> None:
        """Moves this Shutter down for one movement cycle."""
        self.set_state(self.State.DOWN_ONCE)

    def move_down_full(self) -> None:
        """Moves this Shutter down fully."""
        self.set_state(self.State.DOWN_FULL)

    def __str__(self):
        return f"Shutter ({super().__str__()})"


_DEVICE_CLASSES = {I2CApplianceType.BINARY: I2CGenericBinary, 
 I2CApplianceType.DIMMER: I2CDimmer, 
 I2CApplianceType.RGB: I2CRGBDimmer, 
 I2CApplianceType.SHUTTER: I2CShutter}