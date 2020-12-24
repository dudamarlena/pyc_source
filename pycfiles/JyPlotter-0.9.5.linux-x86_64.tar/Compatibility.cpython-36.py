# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.6/site-packages/PyPlotter/Compatibility.py
# Compiled at: 2017-05-19 15:12:17
# Size of source mod 2**32: 2346 bytes
"""Provides code snipplets for ompatibility with older python versions.
"""

def __pragma__(*args):
    pass


__pragma__('skip')
try:
    set
except NameError:
    try:
        import sets
    except ImportError:
        import altsets as sets

    set = sets.Set

try:
    object
except NameError:

    class object:
        pass


import sys
if sys.platform[:4] == 'java':
    if sys.version[:3] == '2.2':

        class object:
            pass


__pragma__('noskip')

def GetDriver(check=[
 'qtGfx', 'gtkGfx', 'wxGfx', 'tkGfx', 'awtGfx']):
    """Get any available Gfx Driver."""
    __pragma__('skip')
    for wish in check:
        if wish == 'qtGfx':
            try:
                import qtGfx
                return qtGfx
            except ImportError:
                try:
                    from . import qtGfx
                    return qtGfx
                except ImportError:
                    pass

        elif wish == 'gtkGfx':
            try:
                import gtkGfx
                return gtkGfx
            except ImportError:
                try:
                    from . import gtkGfx
                    return gtkGfx
                except ImportError:
                    pass

        elif wish == 'wxGfx':
            try:
                import wxGfx
                return wxGfx
            except ImportError:
                pass

        elif wish == 'tkGfx':
            try:
                import tkGfx
                print('WARNING: tk is not fully supported by PyPlotter.\n' + 'Use of wxPython or PyGTK2 is highly recoomended!\n\n')
                return tkGfx
            except ImportError:
                try:
                    from . import tkGfx
                    return tkGfx
                except ImportError:
                    pass

        else:
            if wish == 'awtGfx':
                try:
                    import awtGfx
                    return awtGfx
                except ImportError:
                    pass

    raise ImportError('Could not find a graphics drivers for PyPlotter!\n\n')
    __pragma__('noskip')
    import canvasGfx