# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ana/dev/dexy-clean/dexy/filters/pyn.py
# Compiled at: 2020-03-18 15:12:33
# Size of source mod 2**32: 417 bytes
from dexy.filter import DexyFilter
try:
    import pynliner
    AVAILABLE = True
except ImportError:
    AVAILABLE = False

class PynlinerFilter(DexyFilter):
    __doc__ = '\n    Filter which exposes pynliner for inlining CSS styles into HTML.\n    '
    aliases = ['pyn', 'pynliner']

    def is_active(self):
        return AVAILABLE

    def process_text(self, input_text):
        return pynliner.fromString(input_text)