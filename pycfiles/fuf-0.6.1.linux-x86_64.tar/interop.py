# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/msoucy/.virtualenv/fuf/lib/python2.7/site-packages/fuf/interop.py
# Compiled at: 2014-09-23 17:45:03
import sys
if sys.version_info[0] == 3:
    exec_ = __builtins__['exec']
    raw_input = input
else:

    def exec_(_code_, _globs_=None, _locs_=None):
        """Execute code in a namespace."""
        if _globs_ is None:
            frame = sys._getframe(1)
            _globs_ = frame.f_globals
            if _locs_ is None:
                _locs_ = frame.f_locals
            del frame
        elif _locs_ is None:
            _locs_ = _globs_
        exec 'exec _code_ in _globs_, _locs_'
        return