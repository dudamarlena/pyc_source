# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/self_driving_desktop/recorder.py
# Compiled at: 2019-05-10 22:15:35
# Size of source mod 2**32: 5086 bytes
from __future__ import print_function
import sys, os
from datetime import datetime
from self_driving_desktop.keymap import keymap as KEYMAP
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Xlib import X, XK, display
from Xlib.ext import record
from Xlib.protocol import rq
local_dpy = display.Display()
record_dpy = display.Display()
outfile = None
lasttime = None

def lookup_keysym(keysym):
    for name in dir(XK):
        if name[:3] == 'XK_':
            if getattr(XK, name) == keysym:
                return name[3:]

    return '[%d]' % keysym


def record_callback(reply):
    global lasttime
    global outfile
    if reply.category != record.FromServer:
        return
    else:
        if reply.client_swapped:
            print('* received swapped protocol data, cowardly ignored')
            return
        if not len(reply.data) or reply.data[0] < 2:
            return
    data = reply.data
    while len(data):
        event, data = rq.EventField(None).parse_binary_value(data, record_dpy.display, None, None)
        currtime = datetime.now()
        tdiff = currtime - lasttime
        tmicro = tdiff.microseconds / 1000000.0
        if event.type in [X.KeyPress, X.KeyRelease]:
            pr = event.type == X.KeyPress and 'Press' or 'Release'
            kd = pr == 'Press' and 'd' or 'u'
            outfile.write('  sleep %f;\n' % tmicro)
            keysym = local_dpy.keycode_to_keysym(event.detail, 0)
            if not keysym:
                lasttime = currtime
                key = None
                try:
                    key = KEYMAP[event.detail]
                except:
                    print('Unknown KeyCode:', event.detail)
                    key = event.detail

                outfile.write('  k%s "%s";  # KeyCode\n' % (kd, key))
            else:
                lasttime = currtime
                key1 = lookup_keysym(keysym).lower()
                key = None
                try:
                    key = KEYMAP[key1]
                except:
                    print('Unknown KeyCode:', key1)
                    key = key1

                outfile.write('  k%s "%s";  # KeyStr\n' % (kd, key))
            if event.type == X.KeyPress and keysym == XK.XK_Escape:
                local_dpy.record_disable_context(ctx)
                local_dpy.flush()
                return
        else:
            if event.type == X.ButtonPress:
                lasttime = currtime
                print('ButtonPress', event.detail)
                btn = ''
                if event.detail == 1:
                    btn = 'left'
                else:
                    if event.detail == 2:
                        btn = 'middle'
                    else:
                        if event.detail == 3:
                            btn = 'right'
                outfile.write('  sleep %f;\n' % tmicro)
                outfile.write('  bu "%s";\n' % btn)
            else:
                if event.type == X.ButtonRelease:
                    lasttime = currtime
                    print('ButtonRelease', event.detail)
                    btn = ''
                    if event.detail == 1:
                        btn = 'left'
                    else:
                        if event.detail == 2:
                            btn = 'middle'
                        else:
                            if event.detail == 3:
                                btn = 'right'
                    outfile.write('  sleep %f;\n' % tmicro)
                    outfile.write('  bd "%s";\n' % btn)
                elif event.type == X.MotionNotify:
                    lasttime = currtime
                    print('MotionNotify', event.root_x, event.root_y)
                    outfile.write('  mm %d %d %f;\n' % (event.root_x, event.root_y, tmicro))


if not record_dpy.has_extension('RECORD'):
    print('RECORD extension not found')
    sys.exit(1)
    r = record_dpy.record_get_version(0, 0)
    print('RECORD extension version %d.%d' % (r.major_version, r.minor_version))
ctx = record_dpy.record_create_context(0, [
 record.AllClients], [
 {'core_requests':(0, 0), 
  'core_replies':(0, 0), 
  'ext_requests':(0, 0, 0, 0), 
  'ext_replies':(0, 0, 0, 0), 
  'delivered_events':(0, 0), 
  'device_events':(
   X.KeyPress, X.MotionNotify), 
  'errors':(0, 0), 
  'client_started':False, 
  'client_died':False}])

def do(playlist):
    global lasttime
    global outfile
    try:
        try:
            outfile = open(playlist, 'w+')
            outfile.write('playlist recording {\n')
            lasttime = datetime.now()
            record_dpy.record_enable_context(ctx, record_callback)
            record_dpy.record_free_context(ctx)
        except Exception as e:
            print('Error')
            print(type(e))
            print(e)

    finally:
        outfile.write('};\n\n')
        outfile.write('delay 0.025;\n\n')
        outfile.write('play recording;\n\n')
        outfile.close()