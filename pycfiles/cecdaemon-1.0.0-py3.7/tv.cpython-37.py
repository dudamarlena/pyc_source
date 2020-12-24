# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/cecdaemon/tv.py
# Compiled at: 2018-09-22 12:18:06
# Size of source mod 2**32: 1776 bytes
"""TV control module for cec remote control
"""
import logging
from types import ModuleType
from .const import DEFAULT_TV_CONFIG
logging.getLogger(__name__)

class Tv:
    __doc__ = ' Basic wrapper object for controlling the tv\n\n    :param cec: instance of python-cec\n    :type cec: obj\n    :param tvconf: dictionary of settings\n    :type tvconf: dict\n    '

    def __init__(self, cec=None, tvconf=None):
        if not isinstance(cec, ModuleType):
            raise AssertionError
        else:
            logging.info('Loading tv module')
            self.cec = cec
            self.dev = cec.CECDEVICE_TV
            if tvconf is None:
                logging.warning('No tv section in config, using default')
                self.conf = DEFAULT_TV_CONFIG
            else:
                self.conf = tvconf
        self._set_name()

    def _set_name(self):
        if 'name' in self.conf.keys():
            name = self.conf['name'][:14]
            cec = self.cec
            cec.transmit(cec.CECDEVICE_TV, cec.CEC_OPCODE_SET_OSD_NAME, name)
            logging.info('Device name set to %s', name)

    def volume_up(self):
        """ Increase volume """
        self.cec.volume_up()
        logging.debug('Increased volume')

    def volume_down(self):
        """ Decrease volume """
        self.cec.volume_down()
        logging.debug('Increased volume')

    def toggle_mute(self):
        """ Toggle muting """
        self.cec.toggle_mute()
        logging.debug('Toggled mute')

    def standby(self):
        """ Set tv to standby """
        self.cec.transmit(self.dev, self.cec.CEC_OPCODE_STANDBY)
        logging.debug('Set standby')

    def wakeup(self):
        """ Wake up tv from standby"""
        self.cec.transmit(self.dev, self.cec.CEC_OPCODE_USER_CONTROL_PRESSED, bytes.fromhex('6d'))
        logging.debug('Set wake')