# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/daniel/Desktop/pyInputStats/pyinputstatsmodules/collector.py
# Compiled at: 2011-03-28 13:49:02
import sys, math, time, threading
from Xlib import X, XK, display
from Xlib.ext import record
from Xlib.protocol import rq
from collections import defaultdict
import helpers
DPI = helpers.get_dpi()
print ('Assuming DPI being {0}').format(DPI)
DPC = DPI / 2.54

class DataCollector(object):

    def __init__(self):
        self.last_coords = None
        self.total_distance = 0
        self.total_keys = 0
        self.total_buttons = 0
        self.keys_pressed = defaultdict(int)
        t = threading.Thread(target=self.start_recording)
        t.start()
        return

    def get_data(self):
        if self.total_distance == 0 and self.total_keys == 0 and self.total_buttons == 0:
            return None
        else:
            d = {'distance': self.total_distance, 'keys': self.total_keys, 'buttons': self.total_buttons, 'keys_pressed': self.keys_pressed, 'time': time.time()}
            self.total_distance = 0
            self.total_keys = 0
            self.total_buttons = 0
            self.keys_pressed = defaultdict(int)
            return d

    def start_recording(self):
        self.local_dpy = display.Display()
        self.record_dpy = display.Display()
        r = self.record_dpy.record_get_version(0, 0)
        self.ctx = self.record_dpy.record_create_context(0, [
         record.AllClients], [
         {'core_requests': (0, 0), 
            'core_replies': (0, 0), 
            'ext_requests': (0, 0, 0, 0), 
            'ext_replies': (0, 0, 0, 0), 
            'delivered_events': (0, 0), 
            'device_events': (
                            X.KeyRelease, X.MotionNotify), 
            'errors': (0, 0), 
            'client_started': False, 
            'client_died': False}])
        self.record_dpy.record_enable_context(self.ctx, self.record_callback)
        self.record_dpy.record_free_context(self.ctx)

    def quit(self):
        self.local_dpy.record_disable_context(self.ctx)
        self.local_dpy.flush()

    def record_callback(self, reply):
        if reply['category'] in (4, 5):
            return
        else:
            (event, data) = rq.EventField(None).parse_binary_value(reply.data, self.record_dpy.display, None, None)
            if event.type == X.KeyRelease:
                self.keys_pressed[(event.detail, event.state)] += 1
                self.total_keys += 1
            elif event.type == X.MotionNotify:
                x = event.root_x
                y = event.root_y
                if self.last_coords:
                    xdiff = self.last_coords[0] - x
                    ydiff = self.last_coords[1] - y
                    diff = math.sqrt(xdiff ** 2 + ydiff ** 2)
                    self.total_distance += diff
                    self.last_coords = (x, y)
                else:
                    self.last_coords = (
                     x, y)
            elif event.type == X.ButtonRelease:
                self.total_buttons += 1
            return


if __name__ == '__main__':
    app = DataCollector()