# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bibliopixel/drivers/hue.py
# Compiled at: 2019-08-11 12:22:47
# Size of source mod 2**32: 2592 bytes
from .driver_base import DriverBase
from ..util import log
try:
    from phue import Bridge
except:
    error = 'Unable to import phue. Please install. pip install phue'
    log.error(error)
    raise ImportError(error)

import colorsys

class Hue(DriverBase):
    __doc__ = '\n    Driver for interacting with Philips Hue lights.\n\n    Provides the same parameters of :py:class:`.driver_base.DriverBase` as\n    well as those below:\n\n    :param str ip: Network hostname or IP address of the Hue base.\n    :param list nameMap: List of names to map to each pixel index\n    '

    def __init__(self, num, ip, nameMap=None, **kwds):
        (super().__init__)(num, **kwds)
        if nameMap:
            if len(nameMap) != self.numLEDs:
                raise ValueError('nameMap must have the same number of entries as the number of LEDs.')
        else:
            self._bridge = Bridge(ip)
            self._bridge.connect()
            self._transitionTime = 0
            if nameMap:
                self._lights = self._bridge.get_light_objects('name')
                self._ids = nameMap
            else:
                self._lights = self._bridge.get_light_objects('id')
            self._ids = [l for l in self._lights]
        if len(self._lights) < self.numLEDs:
            raise ValueError('More LEDs were specified than there are available Hue lights.')
        self.setTransitionTime(0)

    def setTransitionTime(self, time):
        if time < 0.0 or time > 30.0:
            raise ValueError('Transition time must be between 0.0 and 30.0 seconds.')
        self._transitionTime = int(time * 10)

    def _mapRange(self, value, minFrom, maxFrom, minTo, maxTo):
        return minTo + (maxTo - minTo) * (value - minFrom) / (maxFrom - minFrom)

    def _rgb2hs(self, rgb):
        r = rgb[0] / 255.0
        g = rgb[1] / 255.0
        b = rgb[2] / 255.0
        h, s, v = colorsys.rgb_to_hsv(r, g, b)
        h = int(self._mapRange(h, 0.0, 1.0, 0, 65535))
        s = int(self._mapRange(s, 0.0, 1.0, 0, 254))
        return (h, s)

    def _send_packet(self):
        for i in range(len(self._ids)):
            h, s = self._rgb2hs(self._colors[(i + self._pos)])
            bri = min(254, self._brightness)
            if s == 0:
                bri = 0
            cmd = {'on':s != 0,  'bri':bri,  'hue':h,  'saturation':s,  'transitiontime':self._transitionTime}
            self._bridge.set_light(self._ids[i], cmd)


from ..util import deprecated
if deprecated.allowed():
    DriverHue = Hue