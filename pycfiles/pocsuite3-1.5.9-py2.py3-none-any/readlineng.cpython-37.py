# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/boyhack/programs/pocsuite3/pocsuite3/lib/core/readlineng.py
# Compiled at: 2019-11-05 01:51:48
# Size of source mod 2**32: 1899 bytes
from pocsuite3.lib.core.data import logger
from pocsuite3.lib.core.exception import PocsuiteSystemException
from pocsuite3.lib.core.settings import IS_WIN
from pocsuite3.lib.core.settings import PLATFORM
_readline = None
try:
    from readline import *
    import readline as _readline
except ImportError:
    try:
        from pyreadline import *
        import pyreadline as _readline
    except ImportError:
        pass

if IS_WIN:
    if _readline:
        try:
            _outputfile = _readline.GetOutputFile()
        except AttributeError:
            debugMsg = "Failed GetOutputFile when using platform's "
            debugMsg += 'readline library'
            logger.debug(debugMsg)
            _readline = None

uses_libedit = False
if PLATFORM == 'mac':
    if _readline:
        import commands
        status, result = commands.getstatusoutput('otool -L %s | grep libedit' % _readline.__file__)
        if status == 0:
            if len(result) > 0:
                _readline.parse_and_bind('bind ^I rl_complete')
                debug_msg = "Leopard libedit detected when using platform's "
                debug_msg += 'readline library'
                logger.debug(debug_msg)
                uses_libedit = True
if _readline:
    try:
        _readline.clear_history()
    except AttributeError:

        def clear_history():
            pass


        _readline.clear_history = clear_history