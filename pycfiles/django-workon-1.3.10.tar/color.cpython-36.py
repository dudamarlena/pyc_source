# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/site-packages/workon/utils/color.py
# Compiled at: 2018-09-19 02:38:32
# Size of source mod 2**32: 1168 bytes
import random
try:
    from colour import Color
except:
    from ._colour import Color

__all__ = [
 'Color', 'PColors', 'rgb_to_hex', 'generate_colors', 'random_color']

class PColors:
    HEADER = '\x1b[95m'
    OKBLUE = '\x1b[94m'
    OKGREEN = '\x1b[92m'
    GREEN = OKGREEN
    WARNING = '\x1b[93m'
    YELLOW = WARNING
    FAIL = '\x1b[91m'
    ERROR = FAIL
    ENDC = '\x1b[0m'
    BOLD = '\x1b[1m'
    UNDERLINE = '\x1b[4m'
    OK = f"{BOLD}{OKGREEN}[OK]{ENDC}"


def rgb_to_hex(rgb_tuple):
    assert len(rgb_tuple) == 3
    denormalized_values = tuple(map(lambda x: 256 * x, rgb_tuple))
    return '#%02x%02x%02x' % denormalized_values


def generate_colors(num, from_color='#f7aabc', to_color='#404a58'):
    """
    Generate `num` distinct Hexadecimal colors
    """
    from_color = Color(from_color)
    to_color = Color(to_color)
    if num == 0:
        return []
    else:
        if num == 1:
            return [
             from_color.hex]
        return list(c.hex for c in from_color.range_to(to_color, num))


def random_color(luminance=0.5):
    import random
    r = lambda : random.randint(0, 255)
    return Color(('#%02X%02X%02X' % (r(), r(), r())), luminance=luminance)