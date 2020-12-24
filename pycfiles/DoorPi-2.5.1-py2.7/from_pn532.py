# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/doorpi/keyboard/from_pn532.py
# Compiled at: 2016-08-01 11:57:45
import logging
logger = logging.getLogger(__name__)
logger.debug('%s loaded', __name__)
import threading
from doorpi.keyboard.AbstractBaseClass import KeyboardAbstractBaseClass, HIGH_LEVEL, LOW_LEVEL
import doorpi, nfc, time

def get(**kwargs):
    return pn532(**kwargs)


class pn532(KeyboardAbstractBaseClass):
    name = 'pn532 nfc keyboard'

    @property
    def current_millisecond_timestamp(self):
        return int(round(time.time() * 1000))

    @property
    def in_bouncetime(self):
        return self.last_key_time + self.bouncetime >= self.current_millisecond_timestamp

    def pn532_recognized(self, tag):
        try:
            try:
                if self.in_bouncetime:
                    logger.debug('founded tag while bouncetime -> skip')
                    return
                self.last_key_time = self.current_millisecond_timestamp
                logger.debug('tag: %s', tag)
                hmm = str(tag)
                ID = str(hmm.split('ID=')[-1:])[2:-2]
                logger.debug('ID: %s', ID)
                if ID in self._InputPins:
                    logger.debug('ID gefunden: %s', ID)
                    self.last_key = ID
                    self._fire_OnKeyDown(self.last_key, __name__)
                    self._fire_OnKeyPressed(self.last_key, __name__)
                    self._fire_OnKeyUp(self.last_key, __name__)
                    doorpi.DoorPi().event_handler('OnFoundKnownTag', __name__)
                    logger.debug('last_key is %s', self.last_key)
            except Exception as ex:
                logger.exception(ex)

        finally:
            logger.debug('pn532_recognized thread ended')

    def pn532_read(self):
        try:
            try:
                while not self._shutdown:
                    self.__clf.connect(rdwr={'on-connect': self.pn532_recognized})

            except Exception as ex:
                logger.exception(ex)

        finally:
            logger.debug('pn532 thread ended')

    def __init__(self, input_pins, output_pins, keyboard_name, conf_pre, conf_post, bouncetime, *args, **kwargs):
        self.keyboard_name = keyboard_name
        self.last_key = ''
        self.bouncetime = bouncetime
        self.last_key_time = self.current_millisecond_timestamp
        section_name = conf_pre + 'keyboard' + conf_post
        self._device = doorpi.DoorPi().config.get_string_parsed(section_name, 'device', 'tty:AMA0:pn532')
        self._InputPins = map(str.upper, input_pins)
        self._InputPairs = {}
        self.__clf = nfc.ContactlessFrontend(self._device)
        for input_pin in self._InputPins:
            self._register_EVENTS_for_pin(input_pin, __name__)
            logger.debug('__init__ (input_pin = %s)', input_pin)

        self._shutdown = False
        self._thread = threading.Thread(target=self.pn532_read)
        self._thread.daemon = True
        self._thread.start()
        self.register_destroy_action()

    def destroy(self):
        if self.is_destroyed:
            return
        else:
            logger.debug('destroy')
            self.__clf.close()
            self.__clf = None
            self._shutdown = True
            doorpi.DoorPi().event_handler.unregister_source(__name__, True)
            self.__destroyed = True
            return

    def status_input(self, tag):
        logger.debug('status_input for tag %s', tag)
        if tag == self.last_key:
            return True
        else:
            return False