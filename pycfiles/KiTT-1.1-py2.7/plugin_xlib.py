# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/kitt/plugin_xlib.py
# Compiled at: 2013-05-30 09:15:32
from kivy.logger import Logger
log = Logger.getChild('KiTT')
from Xlib import X, XK, protocol, display, Xcursorfont
from Xlib.ext import xtest
from Xlib.protocol import request
import os
disp = display.Display()

def grab_mouse():
    log.debug('grab_mouse')
    cursor_font = disp.open_font('cursor')
    cursor = 0
    mycursor = cursor_font.create_glyph_cursor(cursor_font, cursor, cursor + 1, (0,
                                                                                 0,
                                                                                 0), (65535,
                                                                                      65535,
                                                                                      65535))
    disp.screen().root.grab_pointer(False, X.Button4MotionMask | X.Button5MotionMask, X.GrabModeAsync, X.GrabModeAsync, 0, mycursor, X.CurrentTime)
    disp.sync()


def ungrab_mouse():
    log.debug('ungrab_mouse')
    disp.ungrab_pointer(X.CurrentTime)
    disp.sync()


def do_mouse_click(button, target=None):
    """
    executes mouse button click

    :param button: X.Button1, X.Button2 or X.Button3 depending on which button to be triggered
    :param target: list containing name(s) of the target window
    """
    log.debug('do_mouse_click')
    root = disp.screen().root
    pointer_info = request.QueryPointer(display=disp.display, window=root)
    root_xpos, root_ypos = pointer_info._data['root_x'], pointer_info._data['root_y']
    targetwindow = disp.get_input_focus().focus
    if isinstance(button, basestring):
        if button is 'Button1':
            button = X.Button1
        elif button is 'Button2':
            button = X.Button2
        elif button is 'Button3':
            button = X.Button3
        else:
            return False
    elif button not in (X.Button1, X.Button2, X.Button3):
        return False
    if targetwindow.get_wm_name() is None and targetwindow.get_wm_class() is None:
        targetwindow = targetwindow.query_tree().parent
    ret = targetwindow.translate_coords(root, root_xpos, root_ypos)
    target_xpos = ret.x
    target_ypos = ret.y
    if target:
        for target in target:
            if target in targetwindow.get_wm_class():
                break
        else:
            return False

    myevent_press = protocol.event.ButtonPress(detail=button, root=root, root_x=root_xpos, root_y=root_ypos, window=targetwindow.id, event_x=target_xpos, event_y=target_ypos, same_screen=1, state=0, time=X.CurrentTime, child=0)
    myevent_release = protocol.event.ButtonRelease(detail=button, root=root, root_x=root_xpos, root_y=root_ypos, window=targetwindow.id, event_x=target_xpos, event_y=target_ypos, same_screen=1, state=0, time=X.CurrentTime, child=0)
    disp.send_event(X.InputFocus, myevent_press, event_mask=0, propagate=1)
    disp.send_event(X.InputFocus, myevent_release, event_mask=0, propagate=1)
    disp.sync()
    return True


def do_key_press(keys, target=None):
    """
    executes a keypress

    :param keys: argument tuple containing one or several modifier keys, and the key to press
    :param target: list containing name(s) of the target window

    the key to pass as a parameter has to be taken from Xlib.XK library
    """
    log.debug('do_key_press')
    root = disp.screen().root
    keys = map(lambda k: XK.string_to_keysym(k) if isinstance(k, basestring) else k, keys)
    for key in keys:
        if key not in XK.__dict__.values():
            return False

    pointer_info = request.QueryPointer(display=disp.display, window=root)
    root_xpos, root_ypos = pointer_info._data['root_x'], pointer_info._data['root_y']
    targetwindow = disp.get_input_focus().focus
    if targetwindow.get_wm_name() is None and targetwindow.get_wm_class() is None:
        targetwindow = targetwindow.query_tree().parent
    ret = targetwindow.translate_coords(root, root_xpos, root_ypos)
    target_xpos = ret.x
    target_ypos = ret.y
    if target and targetwindow.get_wm_class():
        for t in target:
            if t in targetwindow.get_wm_class():
                break
        else:
            log.info("Window '%s' not found in target(s) %s" % (targetwindow.get_wm_class(), target))
            return False

    def send_key(display, window, keycodes):
        """Send a KeyPress and KeyRelease event"""
        if type(keycodes) not in (tuple, list):
            keycodes = (
             keycodes,)
        for keycode in keycodes:
            xtest.fake_input(window, X.KeyPress, display.keysym_to_keycode(keycode))

        for keycode in reversed(keycodes):
            xtest.fake_input(window, X.KeyRelease, display.keysym_to_keycode(keycode))

        display.sync()

    send_key(disp, root, keys)
    return True


def switch_workspace(direction):
    """
    switches workspace

    :param direction: +1 for next workspace, -1 for previous workspace.
    """
    log.debug('switch_workspace')
    screen = disp.screen()
    root = screen.root
    if isinstance(direction, basestring):
        direction = int(direction)

    def get_property(disp, name):
        atom = disp.intern_atom(name)
        return disp.screen().root.get_full_property(atom, 0)

    def send_event(win, ctype, data, mask=None):
        """ Send a ClientMessage event to the root """
        data = (data + [0] * (5 - len(data)))[:5]
        ev = protocol.event.ClientMessage(window=win, client_type=ctype, data=(32, data))
        if not mask:
            mask = X.SubstructureRedirectMask | X.SubstructureNotifyMask
        root.send_event(ev, event_mask=mask)
        disp.sync()

    cur_ws = get_property(disp, '_NET_CURRENT_DESKTOP').value[0]
    nb_ws = get_property(disp, '_NET_NUMBER_OF_DESKTOPS').value[0]
    if cur_ws + direction < 0:
        cur_ws = nb_ws - 1
    elif cur_ws + direction >= nb_ws:
        cur_ws = 0
    else:
        cur_ws = cur_ws + direction
    send_event(root, display.Display().intern_atom('_NET_CURRENT_DESKTOP'), [
     cur_ws, X.CurrentTime])
    return True


ACTIONS = dict(workspace=switch_workspace, keypress=do_key_press, mouseclick=do_mouse_click)
if __name__ == '__main__':
    import time
    print 'grab_mouse_wheel'
    grab_mouse_wheel()
    time.sleep(1)
    print 'do_mouse_click'
    do_mouse_click(X.Button3)
    time.sleep(1)
    print 'do_key_press'
    do_key_press((XK.XK_Alt_L, XK.XK_Tab))
    time.sleep(1)
    print 'ungrab_mouse_wheel'
    ungrab_mouse_wheel()