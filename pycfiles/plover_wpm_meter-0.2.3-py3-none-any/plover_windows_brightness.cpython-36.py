# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\plover_windows_brightness.py
# Compiled at: 2017-11-12 22:41:10
# Size of source mod 2**32: 1051 bytes
from wmi import WMI
WMI_CONNECTION = WMI(moniker='root/wmi')

def _set_brightness(brightness):
    WMI_CONNECTION.WmiMonitorBrightnessMethods()[0].WmiSetBrightness(brightness, 0)


def _get_brightness():
    return WMI_CONNECTION.WmiMonitorBrightness()[0].CurrentBrightness


def set(engine, brightness):
    brightness = int(brightness)
    assert 0 <= brightness <= 100, 'Brightness can only be 0 to 100'
    _set_brightness(brightness)


def up(engine, increase):
    increase = int(increase) if increase else 10
    assert increase > 0, 'Brightness increase amount must be a positive integer'
    new_brightness = _get_brightness() + increase
    new_brightness = min(new_brightness, 100)
    _set_brightness(new_brightness)


def down(engine, decrease=10):
    decrease = int(decrease) if decrease else 10
    assert decrease > 0, 'Brightness decrease amount must be a positive integer'
    new_brightness = _get_brightness() - decrease
    new_brightness = max(new_brightness, 0)
    _set_brightness(new_brightness)