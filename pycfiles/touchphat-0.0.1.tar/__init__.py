# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ../library/touchphat/__init__.py
# Compiled at: 2017-03-14 09:56:20
import time
from sys import exit
try:
    import cap1xxx
except ImportError:
    exit('This library requires the cap1xxx module\nInstall with: sudo pip install cap1xxx')

__version__ = '0.0.1'
dh = cap1xxx.Cap1166(i2c_addr=44)
auto_leds = True
PADS = list(range(1, 7))
NAMES = [
 'Back', 'A', 'B', 'C', 'D', 'Enter']
LEDMAP = [
 5, 4, 3, 2, 1, 0]
NUMMAP = [
 1, 2, 3, 4, 5, 6]
_on_press = [
 None] * 6
_on_release = [None] * 6

def on_touch(pad, handler=None):
    """Register a function to be called when a pad or pads are hit.

    The function should expect one argument: event. You can look at event.pad to determine which pad was hit.

    :param pad: A single integer 0 to 5, a pad name (Back, A, B, C, D, Enter), or a list
    :param handler: The handler function to call on hit
    """
    global _on_press
    if handler is None:

        def decorate(handler):
            _bind_handler(_on_press, pad, handler)

        return decorate
    else:
        _bind_handler(_on_press, pad, handler)
        return


def on_release(pad, handler=None):
    """Register a function to be called when a pad or pads are released.

    The function should expect one argument: event. You can look at event.pad to determine which pad was released.

    :param pad: A single integer from 0 to 5, a pad name (Back, A, B, C, D, Enter), or a list
    :param handler: The handler function to call on release
    """
    global _on_release
    if handler is None:

        def decorate(handler):
            _bind_handler(_on_release, pad, handler)

        return decorate
    else:
        _bind_handler(_on_release, pad, handler)
        return


def _bind_handler(target, pad, handler):
    if type(pad) == list:
        for p in pad:
            channel = _pad_to_channel(p)
            target[channel] = handler

    else:
        channel = _pad_to_channel(pad)
        target[channel] = handler


def _pad_to_channel(pad):
    try:
        if type(pad) == str:
            return NAMES.index(pad)
        else:
            return NUMMAP.index(pad)

    except ValueError:
        raise TypeError(('Invalid touch pad {}').format(pad))


def _handle_press(event):
    channel = event.channel
    event.name = NAMES[channel]
    event.pad = NUMMAP[channel]
    if auto_leds:
        dh.set_led_state(LEDMAP[channel], True)
    if callable(_on_press[channel]):
        try:
            _on_press[channel](event)
        except TypeError:
            _on_press[channel]()


def _handle_release(event):
    channel = event.channel
    event.name = NAMES[channel]
    event.pad = NUMMAP[channel]
    if auto_leds:
        dh.set_led_state(LEDMAP[channel], False)
    if callable(_on_release[channel]):
        try:
            _on_release[channel](event)
        except TypeError:
            _on_release[channel]()


def led_on(pad):
    """Turn on an LED corresponding to a single pad.

    :param pad: A single integer from 0 to 5 or a pad name (Back, A, B, C, D, Enter), corresponding to the pad whose LED you want to turn on.

    """
    set_led(pad, True)


def all_off():
    """Turn off all LEDs"""
    for pad in PADS:
        led_off(pad)


def all_on():
    """Turn on all LEDs"""
    for pad in PADS:
        led_on(pad)


def led_off(pad):
    """Turn off an LED corresponding to a single pad.

    :param pad: A single integer from 0 to 5 or a pad name (Back, A, B, C, D, Enter), corresponding to the pad whose LED you want to turn off.

    """
    set_led(pad, False)


def set_led(pad, value):
    idx = _pad_to_channel(pad)
    led = LEDMAP[idx]
    dh.set_led_state(led, value)


for x in range(6):
    dh.on(x, event='press', handler=_handle_press)
    dh.on(x, event='release', handler=_handle_release)

dh._write_byte(cap1xxx.R_LED_LINKING, 0)