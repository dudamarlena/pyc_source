# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/fpga_i2c_bridge/sensor.py
# Compiled at: 2020-04-09 04:36:36
# Size of source mod 2**32: 7043 bytes
"""FPGA Sensors representations."""
from __future__ import annotations
from abc import ABC
from enum import Enum
from typing import Any
from fpga_i2c_bridge import UnknownDeviceTypeError, I2CShutter
from fpga_i2c_bridge.util import Logger

class I2CSensorType(Enum):
    __doc__ = 'Enumeration for all sensor types.'
    BUTTON = 1
    TOGGLE = 2
    DIMMER_CYCLE = 3
    RGB_CYCLE = 4
    SHUTTER_CTRL = 5


class I2CSensor(ABC):
    __doc__ = 'Base class for representing a sensor.'

    def __init__(self, bridge: "'I2CBridge'", sensor_id: 'int', sensor_type: 'I2CSensorType'):
        self.bridge = bridge
        self.sensor_id = sensor_id
        self.sensor_type = sensor_type
        self.state = None
        self.logger = Logger.get_logger(self)

    @staticmethod
    def create--- This code section failed: ---

 L.  39         0  SETUP_FINALLY        22  'to 22'

 L.  40         2  LOAD_GLOBAL              _INPUT_CONSTRUCTORS
                4  LOAD_FAST                'sensor_type'
                6  BINARY_SUBSCR    
                8  LOAD_FAST                'bridge'
               10  LOAD_FAST                'sensor_id'
               12  LOAD_FAST                'sensor_type'
               14  LOAD_CONST               ('bridge', 'sensor_id', 'sensor_type')
               16  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               18  POP_BLOCK        
               20  RETURN_VALUE     
             22_0  COME_FROM_FINALLY     0  '0'

 L.  42        22  DUP_TOP          
               24  LOAD_GLOBAL              KeyError
               26  COMPARE_OP               exception-match
               28  POP_JUMP_IF_FALSE    50  'to 50'
               30  POP_TOP          
               32  POP_TOP          
               34  POP_TOP          

 L.  43        36  LOAD_GLOBAL              UnknownDeviceTypeError
               38  LOAD_FAST                'sensor_type'
               40  LOAD_ATTR                value
               42  CALL_FUNCTION_1       1  ''
               44  RAISE_VARARGS_1       1  'exception instance'
               46  POP_EXCEPT       
               48  JUMP_FORWARD         52  'to 52'
             50_0  COME_FROM            28  '28'
               50  END_FINALLY      
             52_0  COME_FROM            48  '48'

Parse error at or near `POP_TOP' instruction at offset 32

    def on_input(self, input_data: 'int') -> 'None':
        """
        Passes input event data to this sensor. Used during polling.
        :param input_data: Input event data
        """
        raise NotImplementedError

    def __str__(self):
        return f"ID {self.sensor_id}"


class I2CBinarySensor(I2CSensor, ABC):
    __doc__ = 'Abstract class for binary sensors (Buttons, Toggles and Cyclers).'

    def __init__(self, *args, **kwargs):
        (super(I2CBinarySensor, self).__init__)(*args, **kwargs)
        self._event_callbacks = {}

    def register_event_handler(self):
        """
        Decorator that registers the following function as a callback that will be called when this sensor emits that
        it has been (de)pressed.
        The function must take one parameter, which will contain the Input event data.
        :return: Decorator
        """

        def decorator(function):

            def wrapper(*args, **kwargs):
                return function(*args, **kwargs)

            self._event_callbacks[function.__name__] = wrapper

        return decorator

    def _fire_event(self, event_data: 'int') -> 'None':
        for func in self._event_callbacks.values():
            func(event_data)


class I2CPassthroughSensor(I2CBinarySensor):
    __doc__ = 'Representation for a sensor that passes through its input (Buttons, Toggles).'

    def __init__(self, *args, **kwargs):
        (super(I2CPassthroughSensor, self).__init__)(*args, **kwargs)

    def on_input(self, input_data: 'int') -> 'None':
        """
        Passes input event data onto this sensor, which it passes through to subscribers.
        :param input_data: Input event data
        """
        self._fire_event(input_data)

    def __str__(self):
        return f"Button ({super().__str__()})"


class I2CCycleButtonSensor(I2CBinarySensor):
    __doc__ = 'Representation for a Cycle sensor (Dimmer Cycle, RGB Cycle).'

    def __init__(self, *args, **kwargs):
        (super(I2CCycleButtonSensor, self).__init__)(*args, **kwargs)

    def on_input(self, input_data: 'int') -> 'None':
        """
        Passes input event data onto this sensor. The data is ignored, and two events (1 and 0) are sent to subscribers
        in short succession.
        :param input_data: Input event data; ignored
        """
        self._fire_event(1)
        self._fire_event(0)

    def __str__(self):
        return f"Button ({super().__str__()})"


class I2CShutterControlSensor(I2CSensor):
    __doc__ = 'Representation for a Shutter Control sensor.'

    def __init__(self, *args, **kwargs):
        (super(I2CShutterControlSensor, self).__init__)(*args, **kwargs)
        self._handlers = {I2CShutter.State.UP_ONCE: {}, 
         I2CShutter.State.UP_FULL: {}, 
         I2CShutter.State.DOWN_ONCE: {}, 
         I2CShutter.State.DOWN_FULL: {}}

    def on_input(self, input_data: 'int') -> 'None':
        """
        Passes input event data to this sensor. The value is a valid Shutter state, and the according subscribers are
        notified about the event.
        :param input_data: Input event data (a valid Shutter state)
        """
        try:
            state = I2CShutter.State(input_data)
            self._call_handlers(state)
        except KeyError as e:
            try:
                self.logger.error(f"Received unknown shutter control input: {e}")
            finally:
                e = None
                del e

    def _register_handler(self, handler_type: 'I2CShutter.State'):

        def decorator(function):

            def wrapper(*args, **kwargs):
                return function(*args, **kwargs)

            self._handlers[handler_type][function.__name__] = wrapper

        return decorator

    def _call_handlers(self, handler_type: 'I2CShutter.State'):
        for func in self._handlers[handler_type].values():
            func()

    def register_short_up_handler(self):
        """
        Decorator that registers the following function as a callback that will be called on every short up press
        emitted from the Shutter control.
        The function must not take any parameters.
        :return: Decorator
        """
        return self._register_handler(I2CShutter.State.UP_ONCE)

    def register_short_down_handler(self):
        """
        Decorator that registers the following function as a callback that will be called on every short down press
        emitted from the Shutter control.
        The function must not take any parameters.
        :return: Decorator
        """
        return self._register_handler(I2CShutter.State.DOWN_ONCE)

    def register_full_up_handler(self):
        """
        Decorator that registers the following function as a callback that will be called on every long up press
        emitted from the Shutter control.
        The function must not take any parameters.
        :return: Decorator
        """
        return self._register_handler(I2CShutter.State.UP_FULL)

    def register_full_down_handler(self):
        """
        Decorator that registers the following function as a callback that will be called on every long down press
        emitted from the Shutter control.
        The function must not take any parameters.
        :return: Decorator
        """
        return self._register_handler(I2CShutter.State.DOWN_FULL)

    def __str__(self):
        return f"Shutter Control ({super().__str__()})"


_INPUT_CONSTRUCTORS = {I2CSensorType.BUTTON: I2CPassthroughSensor, 
 I2CSensorType.TOGGLE: I2CPassthroughSensor, 
 I2CSensorType.DIMMER_CYCLE: I2CCycleButtonSensor, 
 I2CSensorType.RGB_CYCLE: I2CCycleButtonSensor, 
 I2CSensorType.SHUTTER_CTRL: I2CShutterControlSensor}