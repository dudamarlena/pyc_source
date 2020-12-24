# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/doorpi/keyboard/from_rdm6300.py
# Compiled at: 2016-08-01 11:57:45
import logging
logger = logging.getLogger(__name__)
logger.debug('%s loaded', __name__)
import threading, serial, time
from doorpi.keyboard.AbstractBaseClass import KeyboardAbstractBaseClass, HIGH_LEVEL, LOW_LEVEL
import doorpi
START_FLAG = '\x02'
STOP_FLAG = '\x03'
MAX_LENGTH = 14

def get(**kwargs):
    return RDM6300(**kwargs)


class RDM6300(KeyboardAbstractBaseClass):
    name = 'RFID Reader RDM6300'

    @staticmethod
    def calculate_checksum(string):
        checkSum = 0
        for I in range(1, 10, 2):
            checkSum = checkSum ^ (int(string[I], 16) << 4) + int(string[(I + 1)], 16)

        return checkSum

    @staticmethod
    def check_checksum(string):
        given_checksum = (int(string[11], 16) << 4) + int(string[12], 16)
        return given_checksum == RDM6300.calculate_checksum(string)

    def readUART(self):
        while not self._shutdown:
            logger.debug('readUART() started')
            self._UART = serial.Serial(self.__port, self.__baudrate)
            self._UART.timeout = 1
            self._UART.close()
            self._UART.open()
            try:
                try:
                    chars = ''
                    while not self._shutdown:
                        newChar = self._UART.read()
                        if newChar != '':
                            logger.debug('new char %s read', newChar)
                            chars += str(newChar)
                            if newChar == STOP_FLAG and chars[0] == START_FLAG and len(chars) == MAX_LENGTH and RDM6300.check_checksum(chars):
                                logger.debug('found tag, checking dismisstime')
                                now = time.time()
                                if now - self.last_key_time > self.__dismisstime:
                                    doorpi.DoorPi().event_handler('OnFoundTag', __name__)
                                    self.last_key = int(chars[5:-3], 16)
                                    self.last_key_time = now
                                    logger.debug('key is %s', self.last_key)
                                    if self.last_key in self._InputPins:
                                        self._fire_OnKeyDown(self.last_key, __name__)
                                        self._fire_OnKeyPressed(self.last_key, __name__)
                                        self._fire_OnKeyUp(self.last_key, __name__)
                                        doorpi.DoorPi().event_handler('OnFoundKnownTag', __name__)
                                    else:
                                        doorpi.DoorPi().event_handler('OnFoundUnknownTag', __name__)
                            if newChar == STOP_FLAG or len(chars) > MAX_LENGTH:
                                chars = ''

                except Exception as ex:
                    logger.exception(ex)

            finally:
                self._UART.close()
                self._UART = None
                logger.debug('readUART thread ended')

        return

    def __init__(self, input_pins, keyboard_name, conf_pre, conf_post, *args, **kwargs):
        logger.debug('__init__ (input_pins = %s)', input_pins)
        self.keyboard_name = keyboard_name
        self._InputPins = map(int, input_pins)
        doorpi.DoorPi().event_handler.register_event('OnFoundTag', __name__)
        doorpi.DoorPi().event_handler.register_event('OnFoundUnknownTag', __name__)
        doorpi.DoorPi().event_handler.register_event('OnFoundKnownTag', __name__)
        self.last_key = ''
        self.last_key_time = 0
        section_name = conf_pre + 'keyboard' + conf_post
        self.__port = doorpi.DoorPi().config.get(section_name, 'port', '/dev/ttyAMA0')
        self.__baudrate = doorpi.DoorPi().config.get_int(section_name, 'baudrate', 9600)
        self.__dismisstime = doorpi.DoorPi().config.get_int(section_name, 'dismisstime', 5)
        for input_pin in self._InputPins:
            self._register_EVENTS_for_pin(input_pin, __name__)

        self._shutdown = False
        self._thread = threading.Thread(target=self.readUART)
        self._thread.daemon = True
        self._thread.start()
        self.register_destroy_action()

    def destroy(self):
        if self.is_destroyed:
            return
        logger.debug('destroy')
        self._shutdown = True
        doorpi.DoorPi().event_handler.unregister_source(__name__, True)
        self.__destroyed = True

    def status_input(self, tag):
        logger.debug('status_input for tag %s', tag)
        if tag == self.last_key:
            return True
        else:
            return False

    def set_output(self, pin, value, log_output=True):
        return False