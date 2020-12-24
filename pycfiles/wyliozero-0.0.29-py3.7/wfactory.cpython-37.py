# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-armv7l/egg/wyliozero/wfactory.py
# Compiled at: 2019-11-24 09:28:29
# Size of source mod 2**32: 6732 bytes
from gpiozero.pins.rpigpio import RPiGPIOFactory, RPiGPIOPin
from . import winclude as w
from . import main as mainModule

def isRPI(x):
    return w.isR(x) or w.isButton(x) or w.isLED(x)


class WFactory(RPiGPIOFactory):

    def __init__(self):
        super(WFactory, self).__init__()
        self.pin_class = WPin

    def reserve_pins--- This code section failed: ---

 L.  15         0  LOAD_GLOBAL              print
                2  LOAD_FAST                'pins'
                4  CALL_FUNCTION_1       1  '1 positional argument'
                6  POP_TOP          

 L.  16         8  SETUP_LOOP           66  'to 66'
               10  LOAD_FAST                'pins'
               12  GET_ITER         
             14_0  COME_FROM            60  '60'
               14  FOR_ITER             64  'to 64'
               16  STORE_FAST               'spec'

 L.  17        18  LOAD_GLOBAL              isRPI
               20  LOAD_FAST                'spec'
               22  CALL_FUNCTION_1       1  '1 positional argument'
               24  POP_JUMP_IF_FALSE    52  'to 52'

 L.  18        26  LOAD_GLOBAL              super
               28  LOAD_GLOBAL              WFactory
               30  LOAD_FAST                'self'
               32  CALL_FUNCTION_2       2  '2 positional arguments'
               34  LOAD_METHOD              reserve_pins
               36  LOAD_FAST                'requester'
               38  LOAD_GLOBAL              w
               40  LOAD_METHOD              p
               42  LOAD_FAST                'spec'
               44  CALL_METHOD_1         1  '1 positional argument'
               46  CALL_METHOD_2         2  '2 positional arguments'
               48  POP_TOP          
               50  JUMP_BACK            14  'to 14'
             52_0  COME_FROM            24  '24'

 L.  19        52  LOAD_FAST                'spec'
               54  LOAD_GLOBAL              w
               56  LOAD_ATTR                pinsAll
               58  COMPARE_OP               in
               60  POP_JUMP_IF_FALSE    14  'to 14'

 L.  21        62  JUMP_BACK            14  'to 14'
               64  POP_BLOCK        
             66_0  COME_FROM_LOOP        8  '8'

Parse error at or near `POP_BLOCK' instruction at offset 64

    def pin(self, spec):
        if isRPI(spec):
            return super(WFactory, self).pin(w.p(spec))
        if spec in w.pinsAll:
            return self.pin_classselfspec


class WPin(RPiGPIOPin):

    def __init__(self, factory, number):
        self._number = w.p(number)
        self.wnumber = number
        if isRPI(self.wnumber):
            super(WPin, self).__init__factoryw.p(self.wnumber)
        else:
            if w.isDPWM(self.wnumber):
                pass
            elif w.isD(self.wnumber):
                pass
            elif w.isA(self.wnumber):
                pass

    def close(self):
        if isRPI(self.wnumber):
            super(WPin, self).close()
        else:
            if w.isD(self.wnumber):
                if self._get_function() == 'o':
                    mainModule.digitalWriteself.wnumber0

    def output_with_state(self, state):
        if isRPI(self.wnumber):
            super(WPin, self).output_with_state(state)
        else:
            mainModule.pinModeself.wnumber'o'
            mainModule.digitalWriteself.wnumberstate

    def input_with_pull(self, pull):
        if isRPI(self.wnumber):
            super(WPin, self).input_with_pull(pull)
        else:
            mainModule.pinModeself.wnumber'p'

    def _get_function(self):
        if isRPI(self.wnumber):
            return super(WPin, self)._get_function()
        return w.pinState[self.wnumber]

    def _set_function(self, value):
        if isRPI(self.wnumber):
            return super(WPin, self)._set_function(value)
        mainModule.pinModeself.wnumbervalue

    def _get_state(self):
        if isRPI(self.wnumber):
            return super(WPin, self)._get_state()
        if self._get_function() == 'o':
            w.log.error('Trying to get state for pin {0} which is not set for INPUT'.format(self.wnumber))
        else:
            if w.isD(self.wnumber):
                return mainModule.digitalRead(self.wnumber)
            if w.isA(self.wnumber):
                return mainModule.analogRead(self.wnumber)

    def _set_state(self, value):
        if isRPI(self.wnumber):
            super(WPin, self)._set_state(value)
        else:
            if self._get_function() != 'o':
                w.log.error('Trying to set state for pin {0} which is not set for OUTPUT'.format(self.wnumber))
            else:
                if value == int(value):
                    mainModule.digitalWriteself.wnumbervalue
                else:
                    mainModule.analogWriteself.wnumber(value * 255.0)

    def _get_pull(self):
        if isRPI(self.wnumber):
            return super(WPin, self)._get_pull()
        return w.pinState[self.wnumber] == 'p'

    def _set_pull(self, value):
        if isRPI(self.wnumber):
            return super(WPin, self)._set_pull(value)
        elif self._get_function() == 'o':
            w.log.error('Trying to set pullup for pin {0} which is not set for INPUT'.format(self.wnumber))
        else:
            if value != 'up':
                mainModule.pinModeself.wnumber'i'
            else:
                mainModule.pinModeself.wnumber'p'

    def _get_frequency(self):
        if isRPI(self.wnumber):
            super(WPin, self)._get_frequency()
        else:
            print('unimplemented _get_frequency')

    def _set_frequency(self, value):
        if isRPI(self.wnumber):
            super(WPin, self)._set_frequency(value)
        else:
            print('unimplemented _set_frequency')

    def _get_bounce(self):
        super(WPin, self)._get_bounce()

    def _set_bounce(self, value):
        super(WPin, self)._set_bounce(value)

    def _get_edges(self):
        if isRPI(self.wnumber):
            super(WPin, self)._get_edges()
        else:
            return self._edges

    def _set_edges(self, value):
        if isRPI(self.wnumber):
            super(WPin, self)._set_edges(value)
        else:
            f = self.when_changed
            self.when_changed = None
            try:
                self._edges = value
            finally:
                self.when_changed = f

            print('unimplemented _set_edges')

    def _call_when_changed(self, channel):
        super(WPin, self)._call_when_changed(channel)

    def _enable_event_detect(self):
        if isRPI(self.wnumber):
            super(WPin, self)._enable_event_detect()
        else:
            w.addCallback((self.wnumber), (self._edges), callback=(self._call_when_changed), bouncetime=(self._bounce))
            print('unimplemented _enable_event_detect')

    def _disable_event_detect(self):
        if isRPI(self.wnumber):
            super(WPin, self)._disable_event_detect()
        else:
            w.removeCallback(self.wnumber)
            print('unimplemented _disable_event_detect')

    def _set_when_changed(self, value):
        if isRPI(self.wnumber):
            super(WPin, self)._set_when_changed(value)
        else:
            self._when_changed = value
            if hasattr(self, '_edges'):
                _edges = self._edges
            else:
                _edges = None
            if hasattr(self, '_bounce'):
                _bounce = self._bounce
            else:
                _bounce = None
            w.addCallback((self.wnumber), _edges, callback=value, bouncetime=_bounce)
            print('unimplemented _set_when_changed')

    def _get_when_changed(self):
        if isRPI(self.wnumber):
            return super(WPin, self)._get_when_changed()
        print('unimplemented _get_when_changed')
        if hasattr(self, '_when_changed'):
            print('pl')
            return self._when_changed
        print('nue')
        return