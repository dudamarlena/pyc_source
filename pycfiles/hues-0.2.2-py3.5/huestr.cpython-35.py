# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/hues/huestr.py
# Compiled at: 2016-10-02 05:22:47
# Size of source mod 2**32: 1494 bytes
import sys
from functools import partial
from .colortable import FG, BG, HI_FG, HI_BG, SEQ, STYLE, KEYWORDS
from .dpda import zero_break, annihilator, dedup, apply
if sys.version_info.major == 2:
    str = unicode
OPTIMIZATION_STEPS = (
 zero_break,
 annihilator(FG + HI_FG),
 annihilator(BG + HI_BG),
 dedup)
optimize = partial(apply, OPTIMIZATION_STEPS)

def colorize(string, stack):
    """Apply optimal ANSI escape sequences to the string."""
    codes = optimize(stack)
    if len(codes):
        prefix = SEQ % ';'.join(map(str, codes))
        suffix = SEQ % STYLE.reset
        return prefix + string + suffix
    else:
        return string


class HueString(str):
    __doc__ = 'Extend the string class to support hues.'

    def __new__(cls, string, hue_stack=None):
        """Return a new instance of the class."""
        return super(HueString, cls).__new__(cls, string)

    def __init__(self, string, hue_stack=tuple()):
        self._HueString__string = string
        self._HueString__hue_stack = hue_stack

    def __getattr__(self, attr):
        try:
            code = getattr(KEYWORDS, attr)
            hues = self._HueString__hue_stack + (code,)
            return HueString(self._HueString__string, hue_stack=hues)
        except AttributeError as e:
            raise e

    @property
    def colorized(self):
        return colorize(self._HueString__string, self._HueString__hue_stack)