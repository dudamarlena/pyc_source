# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/doorpi/sipphone/pjsua_lib/SipPhoneCallCallBack.py
# Compiled at: 2016-08-01 11:57:45
import logging
logger = logging.getLogger(__name__)
logger.debug('%s loaded', __name__)
import threading, datetime, time, os, pjsua as pj
from doorpi import DoorPi

class SipPhoneCallCallBack(pj.CallCallback):
    Lib = None
    __DTMF = ''
    __possible_DTMF = []

    def __init__(self, PlayerID=None, call=None):
        logger.debug('__init__')
        self.PlayerID = PlayerID
        self.Lib = pj.Lib.instance()
        DoorPi().event_handler.register_event('OnCallMediaStateChange', __name__)
        DoorPi().event_handler.register_event('OnCallStateChange', __name__)
        DoorPi().event_handler.register_event('OnCallStateConnect', __name__)
        DoorPi().event_handler.register_event('AfterCallStateConnect', __name__)
        DoorPi().event_handler.register_event('OnCallStateDisconnect', __name__)
        DoorPi().event_handler.register_event('AfterCallStateDisconnect', __name__)
        DoorPi().event_handler.register_event('OnCallStateDismissed', __name__)
        DoorPi().event_handler.register_event('OnCallStart', __name__)
        DoorPi().event_handler.register_event('OnDTMF', __name__)
        self.__possible_DTMF = DoorPi().config.get_keys('DTMF')
        for DTMF in self.__possible_DTMF:
            DoorPi().event_handler.register_event('OnDTMF_' + DTMF, __name__)

        DoorPi().event_handler('OnCallStart', __name__)

    def __del__(self):
        self.destroy()

    def destroy(self):
        logger.debug('destroy')
        DoorPi().event_handler.unregister_source(__name__, True)

    def on_media_state(self):
        logger.debug('on_media_state (%s)', str(self.call.info().media_state))
        DoorPi().event_handler('OnCallMediaStateChange', __name__, {'remote_uri': self.call.info().remote_uri, 
           'media_state': str(self.call.info().media_state)})

    def on_state(self):
        logger.debug('on_state (%s)', self.call.info().state_text)
        DoorPi().event_handler('OnCallStateChange', __name__, {'remote_uri': self.call.info().remote_uri, 
           'state': self.call.info().state_text})
        if self.call.info().state in [pj.CallState.CONFIRMED] and self.call.info().media_state == pj.MediaState.ACTIVE:
            DoorPi().event_handler('OnCallStateConnect', __name__, {'remote_uri': self.call.info().remote_uri})
            call_slot = self.call.info().conf_slot
            self.Lib.conf_connect(call_slot, 0)
            self.Lib.conf_connect(0, call_slot)
            logger.debug('conneted Media to call_slot %s', str(call_slot))
            DoorPi().event_handler('AfterCallStateConnect', __name__, {'remote_uri': self.call.info().remote_uri})
        if self.call.info().state == pj.CallState.DISCONNECTED:
            call_slot = self.call.info().conf_slot
            if call_slot > -1:
                DoorPi().event_handler('OnCallStateDisconnect', __name__, {'remote_uri': self.call.info().remote_uri})
                self.Lib.conf_disconnect(call_slot, 0)
                self.Lib.conf_disconnect(0, call_slot)
                logger.debug('disconneted Media from call_slot %s', str(call_slot))
                DoorPi().event_handler('AfterCallStateDisconnect', __name__, {'remote_uri': self.call.info().remote_uri})
            else:
                DoorPi().event_handler('OnCallStateDismissed', __name__, {'remote_uri': self.call.info().remote_uri})

    def on_dtmf_digit(self, digits):
        logger.debug('on_dtmf_digit (%s)', str(digits))
        self.__DTMF += str(digits)
        for DTMF in self.__possible_DTMF:
            if self.__DTMF.endswith(DTMF[1:-1]):
                DoorPi().event_handler('OnDTMF_' + DTMF + '', __name__, {'remote_uri': str(self.call.info().remote_uri), 
                   'DTMF': str(self.__DTMF)})