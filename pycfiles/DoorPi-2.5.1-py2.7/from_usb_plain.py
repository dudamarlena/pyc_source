# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/doorpi/keyboard/from_usb_plain.py
# Compiled at: 2016-08-01 11:57:45
import logging
logger = logging.getLogger(__name__)
logger.debug('%s loaded', __name__)
import threading, serial, time
from os import linesep as OS_LINESEP
from doorpi.keyboard.AbstractBaseClass import KeyboardAbstractBaseClass, HIGH_LEVEL, LOW_LEVEL
import doorpi
CONFIG = doorpi.DoorPi().config

def get(**kwargs):
    return UsbPlain(**kwargs)


class UsbPlain(KeyboardAbstractBaseClass):
    name = 'UsbPlain Keyboard'

    @property
    def last_received_chars(self):
        return self._last_received_chars

    _ser = None

    def read_usb_plain(self):
        self._last_received_chars = ''
        while not self._shutdown and self._ser.isOpen():
            newChar = self._ser.read()
            if newChar == '':
                continue
            self._last_received_chars += str(newChar)
            logger.debug('new char %s read and is now %s', newChar, self._last_received_chars)
            for input_pin in self._InputPins:
                if self._last_received_chars.endswith(input_pin):
                    self.last_key = input_pin
                    self._fire_OnKeyDown(input_pin, __name__)
                    self._fire_OnKeyPressed(input_pin, __name__)
                    self._fire_OnKeyUp(input_pin, __name__)

            if self._last_received_chars.endswith(self._input_stop_flag):
                logger.debug('found input stop flag -> clear received chars')
                self._last_received_chars = ''
            if len(self._last_received_chars) > self._input_max_size:
                logger.debug('received chars bigger then input max size -> clear received chars')
                self._last_received_chars = ''

    def __init__(self, input_pins, output_pins, conf_pre, conf_post, keyboard_name, *args, **kwargs):
        logger.debug('FileSystem.__init__(input_pins = %s, output_pins = %s)', input_pins, output_pins)
        self.keyboard_name = keyboard_name
        self._InputPins = map(str, input_pins)
        self._OutputPins = map(str, output_pins)
        self._last_received_chars = ''
        self.last_key = ''
        for input_pin in self._InputPins:
            self._register_EVENTS_for_pin(input_pin, __name__)

        for output_pin in self._OutputPins:
            self.set_output(output_pin, 0, False)

        section_name = conf_pre + 'keyboard' + conf_post
        port = CONFIG.get(section_name, 'port', '/dev/ttyUSB0')
        baudrate = CONFIG.get_int(section_name, 'baudrate', 9600)
        self._input_stop_flag = CONFIG.get(section_name, 'input_stop_flag', OS_LINESEP)
        self._input_max_size = CONFIG.get_int(section_name, 'input_max_size', 255)
        self._output_stop_flag = CONFIG.get(section_name, 'output_stop_flag', OS_LINESEP)
        self._ser = serial.Serial(port, baudrate)
        self._ser.timeout = 1
        self._ser.close()
        self._ser.open()
        self._shutdown = False
        self._thread = threading.Thread(target=self.read_usb_plain)
        self._thread.daemon = True
        self._thread.start()
        doorpi.DoorPi().event_handler.register_action('OnShutdown', self.destroy)

    def destroy(self):
        if self.is_destroyed:
            return
        logger.debug('destroy')
        self._shutdown = True
        if self._ser and self._ser.isOpen():
            self._ser.close()
        doorpi.DoorPi().event_handler.unregister_source(__name__, True)
        self.__destroyed = True

    def status_input(self, input_pin):
        logger.debug('status_input for tag %s', tag)
        if input_pin == self.last_key:
            return True
        else:
            return False

    def set_output(self, pin, value, log_output=True):
        if self._ser and self._ser.isOpen():
            if log_output:
                logger.debug('try to write %s to serial usb plain', pin)
            self._ser.flushOutput()
            self._ser.write(pin + self._output_stop_flag)
            self._ser.flush()
            return True
        else:
            if log_output:
                logger.warning("couldn't write to serial usb plain, because it's not open")
            return False