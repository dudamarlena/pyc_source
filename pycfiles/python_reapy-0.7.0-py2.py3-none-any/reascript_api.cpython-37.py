# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\despres\Desktop\reaper\scripts\reapy\reapy\reascript_api.py
# Compiled at: 2020-05-09 09:40:15
# Size of source mod 2**32: 1204 bytes
import reapy
from reapy.tools import json
import sys

@reapy.inside_reaper()
def _get_api_names():
    return __all__


if reapy.is_inside_reaper():
    import reaper_python as _RPR
    __all__ = [s[4:] for s in _RPR.__dict__ if s.startswith('RPR_')]
    for s in __all__:
        exec("{} = _RPR.__dict__['{}']".format(s, 'RPR_' + s))

    from reapy import additional_api as _A_API
    for s in _A_API.__dict__:
        exec('from reapy.additional_api import {}'.format(s))

    try:
        import sws_python as _SWS
        sws_functions = set(_SWS.__dict__) - set(_RPR.__dict__)
        __all__ += list(sws_functions)
        for s in sws_functions:
            exec('from sws_python import {}'.format(s))

    except ModuleNotFoundError:
        pass

else:
    if reapy.dist_api_is_enabled():
        __all__ = _get_api_names()
        func_def = '@reapy.inside_reaper()\ndef {name}(*args): return (name)(*args)'
        exec('\n'.join((func_def.format(name=name) for name in __all__)))
        del func_def