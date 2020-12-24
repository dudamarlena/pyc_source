# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/daniel/Programming/python/joy2mouse/joy2mouselib/joystick.py
# Compiled at: 2011-06-08 11:30:04
""" 
Copyright 2009 Jezra Lickter 
 
This software is distributed AS IS. Use at your own risk. 
If it borks your system, you have  been forewarned. 
 
This software is licensed under the LGPL Version 3 
http://www.gnu.org/licenses/lgpl-3.0.txt 
 
 
for documentation on Linux Joystick programming please see 
http://www.mjmwired.net/kernel/Documentation/input/joystick-api.txt 
"""
import gobject, struct

class Joystick(gobject.GObject):
    """The Joystick class is a GObject that sends signals that represent 
    Joystick events"""
    EVENT_BUTTON = 1
    EVENT_AXIS = 2
    EVENT_INIT = 128
    EVENT_FORMAT = 'IhBB'
    EVENT_SIZE = struct.calcsize(EVENT_FORMAT)
    __gsignals__ = {'axis': (
              gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE,
              (
               gobject.TYPE_INT, gobject.TYPE_INT, gobject.TYPE_INT)), 
       'button': (
                gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE,
                (
                 gobject.TYPE_INT, gobject.TYPE_INT, gobject.TYPE_INT))}

    def __init__(self, device):
        gobject.GObject.__init__(self)
        try:
            self.device = open(device)
            gobject.io_add_watch(self.device, gobject.IO_IN, self.read_buttons)
        except IOError:
            raise
        except Exception as ex:
            raise Exception(ex)

    def read_buttons(self, arg0='', arg1=''):
        """ read the button and axis press event from the joystick device 
        and emit a signal containing the event data 
        """
        read_event = self.device.read(self.EVENT_SIZE)
        time, value, type, number = struct.unpack(self.EVENT_FORMAT, read_event)
        event = type & ~self.EVENT_INIT
        init = type & ~event
        if event == self.EVENT_AXIS:
            signal = 'axis'
        elif event == self.EVENT_BUTTON:
            signal = 'button'
        if signal:
            self.emit(signal, number, value, init)
        return True


if __name__ == '__main__':
    try:
        j = Joystick(0)
        loop = gobject.MainLoop()
        loop.run()
    except Exception as e:
        print e