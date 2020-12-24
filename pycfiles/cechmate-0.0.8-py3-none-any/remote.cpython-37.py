# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/cecdaemon/remote.py
# Compiled at: 2018-09-22 12:11:41
# Size of source mod 2**32: 3197 bytes
__doc__ = 'Remote module for cec remote control\n'
import logging, uinput
from .const import DEFAULT_REMOTE_CONFIG
logging.getLogger(__name__)

class Remote:
    """Remote"""

    def __init__(self, cec=None, keymap=None):
        self.callbacks = {}
        self.keystate = None
        if keymap is None:
            logging.warning('No keymap found in config, using default')
            self.keymap = DEFAULT_REMOTE_CONFIG
        else:
            self.keymap = keymap
        cec.add_callback(self.eventrouter, cec.EVENT_KEYPRESS)
        devicekeys = []
        for key, value in self.keymap.items():
            devicekeys.append(getattr(uinput, value))

        self.device = uinput.Device(devicekeys)
        logging.info('Remote initialized')

    def eventrouter(self, event, key, state):
        """ Takes a cec event and routes it to the appropriate handler

        :int event: should be 2 for keypresses
        :int key: number representing the key pressed
        :int state: 0 for down, otherwise time held before release in ms
        """
        if not event == 2:
            raise AssertionError
        elif key in self.callbacks:
            self.callbacks[key](key, state)
        elif str(key) in self.keymap:
            self.keypress(event, key, state)
        else:
            logging.info('Key not mapped: %i', key)

    def keypress(self, event, key, state):
        """ Takes a cec remote event and outputs a keystroke

        :param event: should be 2
        :type event: int
        :param key: number representing the key pressed
        :type key: int
        :param state: 0 for down, otherwise time held before release in ms
        :type state: int
        """
        assert event == 2
        keycode = getattr(uinput, self.keymap[str(key)])
        if state == 0:
            if self.keystate is None:
                logging.debug('%i is mapped to %s', key, self.keymap[str(key)])
                logging.debug('Key %i down', key)
                self.keystate = 'down'
                self.device.emit(keycode, 1)
        if state > 0:
            if self.keystate is None:
                logging.debug('Key %i down', key)
                self.device.emit(keycode, 1)
            logging.debug('Key %i up after %ims', key, state)
            self.device.emit(keycode, 0)
            self.keystate = None

    def add_callback(self, function, key):
        """ Takes a function and a key and adds a callback when that
            key is pressed

        :param function: the function to call when key is pressed
        :type function: func
        :param key: number representing the key pressed
        :type key: int
        """
        self.callbacks[key] = function
        logging.debug('Added callback')
        logging.debug(self.callbacks)