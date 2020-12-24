# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/danyvohl/code/shwirl/extern/vispy/util/fonts/_triage.py
# Compiled at: 2017-04-05 22:12:59
# Size of source mod 2**32: 1130 bytes
import sys
from ._vispy_fonts import _vispy_fonts
if sys.platform.startswith('linux'):
    from ._freetype import _load_glyph
    from ...ext.fontconfig import _list_fonts
else:
    if sys.platform == 'darwin':
        from ._quartz import _load_glyph, _list_fonts
    else:
        if sys.platform.startswith('win'):
            from ._freetype import _load_glyph
            from ._win32 import _list_fonts
        else:
            raise NotImplementedError('unknown system %s' % sys.platform)
_fonts = {}

def list_fonts():
    """List system fonts

    Returns
    -------
    fonts : list of str
        List of system fonts.
    """
    vals = _list_fonts()
    for font in _vispy_fonts:
        vals += [font] if font not in vals else []

    vals = sorted(vals, key=lambda s: s.lower())
    return vals