# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Kamaelia/Automata/Behaviours.py
# Compiled at: 2008-10-19 12:19:52
"""=================
Simple behaviours
=================

A collection of components that send to their "outbox" outbox, values according
to simple behaviours - such as constant value, bouncing, looping etc.

Example Usage
-------------

Generate values that bounce up and down between 0 and 1 in steps of 0.05::

    bouncingFloat(scale_speed=0.05*10)

Generate (x,y) coordinates, starting at (50,50) that bounce within a 200x100 box
with a 10 unit inside margin::

    cartesianPingPong(point=(50,50), width=200, height=100, border=10)

Generate the angles for the seconds hand on an analog watch::

    loopingCounter(increment=360/60, modulo=360)

Constantly generate the number 7::

    continuousIdentity(original=7)

Constantly generate the string "hello"::

    continuousIdentity(original="hello")

Constantly generate the value 0::

    continuousZero()
    
Constantly generate the value 1::

    continuousOne()

    
More detail
-----------

All components start emitting values as soon as they are activated. They then
emit values as fast as they can (there is no throttling/rate control).

All components will terminate if they receive the string "shutdown" on their
"control" inbox. They also then send "shutdown" to their "signal" outbox.

All components will pause and stop emitting values if they receive the string
"pause" on their "control" inbox. They will resume from where they left off if
they receive the string "unpause" on the same inbox.

"""
from Axon.Component import component
send_one_component = component

class bouncingFloat(send_one_component):
    """   bouncingFloat(scale_speed) -> new bouncingFloat component

   A component that emits a value that constantly bounces between 0 and 1.
   
   scale_speed scales the rate at which the value changes. 1.0 = tenths,
   0.5 = twentieths, etc.
   """

    def __init__(self, scale_speed):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
        super(bouncingFloat, self).__init__()
        self.scale_speed = scale_speed

    def main(self):
        """Main loop"""
        scale = 1.0
        direction = 1
        while 1:
            scale = scale + 0.1 * self.scale_speed * direction
            if scale > 1.0:
                scale = 1.05
                direction = direction * -1
            if scale < 0.1:
                scale = 0.05
                direction = direction * -1
            self.send(scale, 'outbox')
            if self.dataReady('control'):
                data = self.recv('control')
                if data == 'shutdown':
                    self.send('shutdown', 'signal')
                    return
                if data == 'pause':
                    self.pause()
                if data == 'unpause':
                    pass
            yield 1


class cartesianPingPong(send_one_component):
    """   cartesianPingPong(point,width,height,border) -> new cartesianPingPong component

   A component that emits (x,y) values that bounce around within the specified
   bounds.

   Keyword arguments:
   
   - point          -- starting (x,y) coordinates
   - width, height  -- bounds of the area
   - border         -- distance in from bounds at which bouncing happens
   """

    def __init__(self, point, width, height, border):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
        super(cartesianPingPong, self).__init__()
        self.point = point
        self.width = width
        self.height = height
        self.border = border

    def main(self):
        """Main loop."""
        delta_y = 10
        delta_x = 10
        while 1:
            self.point[0] = self.point[0] + delta_x
            self.point[1] = self.point[1] + delta_y
            if self.point[0] > self.width - self.border:
                delta_x = -10
            if self.point[0] < self.border:
                delta_x = 10
            if self.point[1] > self.height - self.border:
                delta_y = -10
            if self.point[1] < self.border:
                delta_y = 10
            self.send([ x for x in self.point ], 'outbox')
            if self.dataReady('control'):
                data = self.recv('control')
                if data == 'shutdown':
                    self.send('shutdown', 'signal')
                    return
                if data == 'pause':
                    self.pause()
                if data == 'unpause':
                    pass
            yield 1


class loopingCounter(send_one_component):
    """   loopingCounter(increment[,modulo]) -> new loopingCounter component

   Emits an always incrementing value, that wraps back to zero when it reaches
   the specified limit.

   Keyword arguments:
   - increment  -- increment step size
   - modulo     -- counter wrap back to zero before reaching this value (default=360)
   """

    def __init__(self, increment, modulo=360):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
        super(loopingCounter, self).__init__()
        self.increment = increment
        self.modulo = modulo

    def main(self):
        """Main loop."""
        total = 0
        while 1:
            total = (total + self.increment) % self.modulo
            self.send(total, 'outbox')
            if self.dataReady('control'):
                data = self.recv('control')
                if data == 'shutdown':
                    self.send('shutdown', 'signal')
                    return
                if data == 'pause':
                    self.pause()
                if data == 'unpause':
                    pass
            yield 1


class continuousIdentity(send_one_component):
    """   continuousIdentity(original) -> new continuousIdentity component

   A component that constantly emits the original value.
   """

    def __init__(self, original, *args):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
        super(continuousIdentity, self).__init__()
        self.original = original

    def main(self):
        """Main loop."""
        while 1:
            self.send(self.original, 'outbox')
            if self.dataReady('control'):
                data = self.recv('control')
                if data == 'shutdown':
                    self.send('shutdown', 'signal')
                    return
                if data == 'pause':
                    self.pause()
                if data == 'unpause':
                    pass
            yield 1


class continuousZero(send_one_component):
    """   continuousZero() -> new continuousZero component

   A component that constantly emits the value 0.
   """

    def __init__(self, *args):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
        super(continuousZero, self).__init__()

    def main(self):
        """Main loop."""
        while 1:
            self.send(0, 'outbox')
            if self.dataReady('control'):
                data = self.recv('control')
                if data == 'shutdown':
                    self.send('shutdown', 'signal')
                    return
                if data == 'pause':
                    self.pause()
                if data == 'unpause':
                    pass
            yield 1


class continuousOne(send_one_component):
    """   continuousOne() -> new continuousOne component

   A component that constantly emits the value 1.
   """

    def __init__(self, *args):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
        super(continuousOne, self).__init__()

    def main(self):
        """Main loop."""
        while 1:
            self.send(1, 'outbox')
            if self.dataReady('control'):
                data = self.recv('control')
                if data == 'shutdown':
                    self.send('shutdown', 'signal')
                    return
                if data == 'pause':
                    self.pause()
                if data == 'unpause':
                    pass
            yield 1


__kamaelia_components__ = (bouncingFloat, cartesianPingPong, loopingCounter, continuousIdentity, continuousZero, continuousOne)