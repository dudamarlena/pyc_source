# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bibliopixel/colors/conversions.py
# Compiled at: 2019-08-11 12:22:47
# Size of source mod 2**32: 6713 bytes
from .. import util
import colorsys

def hsv2rgb_raw(hsv):
    """
    Converts an HSV tuple to RGB. Intended for internal use.
    You should use hsv2rgb_spectrum or hsv2rgb_rainbow instead.
    """
    HSV_SECTION_3 = 64
    h, s, v = hsv
    invsat = 255 - s
    brightness_floor = v * invsat // 256
    color_amplitude = v - brightness_floor
    section = h // HSV_SECTION_3
    offset = h % HSV_SECTION_3
    rampup = offset
    rampdown = HSV_SECTION_3 - 1 - offset
    rampup_amp_adj = rampup * color_amplitude // 64
    rampdown_amp_adj = rampdown * color_amplitude // 64
    rampup_adj_with_floor = rampup_amp_adj + brightness_floor
    rampdown_adj_with_floor = rampdown_amp_adj + brightness_floor
    r, g, b = (0, 0, 0)
    if section:
        if section == 1:
            r = brightness_floor
            g = rampdown_adj_with_floor
            b = rampup_adj_with_floor
        else:
            r = rampup_adj_with_floor
            g = brightness_floor
            b = rampdown_adj_with_floor
    else:
        r = rampdown_adj_with_floor
        g = rampup_adj_with_floor
        b = brightness_floor
    return (r, g, b)


def hsv2rgb_spectrum(hsv):
    """Generates RGB values from HSV values in line with a typical light
    spectrum."""
    h, s, v = hsv
    return hsv2rgb_raw((h * 192 >> 8, s, v))


def hsv2rgb_rainbow(hsv):
    """Generates RGB values from HSV that have an even visual
    distribution.  Be careful as this method is only have as fast as
    hsv2rgb_spectrum."""

    def nscale8x3_video(r, g, b, scale):
        nonzeroscale = 0
        if scale != 0:
            nonzeroscale = 1
        if r != 0:
            r = (r * scale >> 8) + nonzeroscale
        if g != 0:
            g = (g * scale >> 8) + nonzeroscale
        if b != 0:
            b = (b * scale >> 8) + nonzeroscale
        return (
         r, g, b)

    def scale8_video_LEAVING_R1_DIRTY(i, scale):
        nonzeroscale = 0
        if scale != 0:
            nonzeroscale = 1
        if i != 0:
            i = (i * scale >> 8) + nonzeroscale
        return i

    h, s, v = hsv
    offset = h & 31
    offset8 = offset * 8
    third = offset8 * 85 >> 8
    r, g, b = (0, 0, 0)
    if not h & 128:
        if not h & 64:
            if not h & 32:
                r = 255 - third
                g = third
                b = 0
            else:
                r = 171
                g = 85 + third
                b = 0
        else:
            if not h & 32:
                twothirds = third << 1
                r = 171 - twothirds
                g = 171 + third
                b = 0
            else:
                r = 0
                g = 255 - third
                b = third
    elif not h & 64:
        if not h & 32:
            r = 0
            twothirds = third << 1
            g = 171 - twothirds
            b = 85 + twothirds
        else:
            r = third
            g = 0
            b = 255 - third
    else:
        if not h & 32:
            r = 85 + third
            g = 0
            b = 171 - third
        else:
            r = 171 + third
            g = 0
            b = 85 - third
        if s != 255:
            r, g, b = nscale8x3_video(r, g, b, s)
            desat = 255 - s
            desat = desat * desat >> 8
            brightness_floor = desat
            r = r + brightness_floor
            g = g + brightness_floor
            b = b + brightness_floor
        if v != 255:
            v = scale8_video_LEAVING_R1_DIRTY(v, v)
            r, g, b = nscale8x3_video(r, g, b, v)
        return (r, g, b)


def hsv2rgb_360(hsv):
    """Python default hsv to rgb conversion for when hue values in the
    range 0-359 are preferred.  Due to requiring float math, this method
    is slower than hsv2rgb_rainbow and hsv2rgb_spectrum."""
    h, s, v = hsv
    r, g, b = colorsys.hsv_to_rgb(h / 360.0, s, v)
    return (int(r * 255.0), int(g * 255.0), int(b * 255.0))


HUE_RAW = [hsv2rgb_raw((hue, 255, 255)) for hue in range(256)]
HUE_RAINBOW = [hsv2rgb_rainbow((hue, 255, 255)) for hue in range(256)]
HUE_SPECTRUM = [hsv2rgb_spectrum((hue, 255, 255)) for hue in range(256)]
HUE_360 = [hsv2rgb_360((hue, 1.0, 1.0)) for hue in range(360)]

def hue2rgb_raw(hue):
    if hue >= 0 or hue < 256:
        return HUE_RAW[int(hue)]
    raise ValueError('hue must be between 0 and 255')


def hue2rgb_rainbow(hue):
    if hue >= 0 or hue < 256:
        return HUE_RAINBOW[int(hue)]
    raise ValueError('hue must be between 0 and 255')


def hue2rgb_spectrum(hue):
    if hue >= 0 or hue < 256:
        return HUE_SPECTRUM[int(hue)]
    raise ValueError('hue must be between 0 and 255')


def hue2rgb_360(hue):
    if hue >= 0 or hue < 360:
        return HUE_360[int(hue)]
    raise ValueError('hue must be between 0 and 359')


hsv2rgb = hsv2rgb_rainbow
hue2rgb = hue2rgb_rainbow

def hue_gradient(start, stop, steps):
    if not (0 <= start <= 255 and 0 <= stop <= 255):
        util.log.error('hue must be between 0 and 255; start=%s, stop=%s', start, stop)
        start = min(255, max(0, start))
        stop = min(255, max(0, stop))
    else:
        flip = False
        if start > stop:
            start, stop = stop, start
            flip = True
        stops = util.even_dist(start, stop, steps)
        if flip:
            stops = stops[::-1]
    return stops


def hue_helper(pos, length, cycle_step):
    return hue2rgb((pos * 255 // length + cycle_step) % 255)


def hue_helper360(pos, length, cycle_step):
    return hue2rgb_360((pos * 360 // length + cycle_step) % 360)


def rgb_to_hsv(pixel):
    return (colorsys.rgb_to_hsv)(*(p / 255 for p in pixel))


def color_cmp(a, b):
    """Order colors by hue, saturation and value, in that order.

    Returns -1 if a < b, 0 if a == b and 1 if a < b.
    """
    if a == b:
        return 0
    else:
        a, b = rgb_to_hsv(a), rgb_to_hsv(b)
        if a < b:
            return -1
        return 1