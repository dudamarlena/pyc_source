# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dani/Documents/Projects/Golismero_2.0/src_github/tools/sqlmap/lib/core/readlineng.py
# Compiled at: 2013-12-09 06:41:17
"""
Copyright (c) 2006-2013 sqlmap developers (http://sqlmap.org/)
See the file 'doc/COPYING' for copying permission
"""
from lib.core.data import logger
from lib.core.settings import IS_WIN
from lib.core.settings import PLATFORM
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

if IS_WIN and _readline:
    try:
        _outputfile = _readline.GetOutputFile()
    except AttributeError:
        debugMsg = "Failed GetOutputFile when using platform's "
        debugMsg += 'readline library'
        logger.debug(debugMsg)
        _readline = None

uses_libedit = False
if PLATFORM == 'mac' and _readline:
    import commands
    status, result = commands.getstatusoutput('otool -L %s | grep libedit' % _readline.__file__)
    if status == 0 and len(result) > 0:
        _readline.parse_and_bind('bind ^I rl_complete')
        debugMsg = "Leopard libedit detected when using platform's "
        debugMsg += 'readline library'
        logger.debug(debugMsg)
        uses_libedit = True
if _readline:
    try:
        _readline.clear_history()
    except AttributeError:

        def clear_history():
            pass


        _readline.clear_history = clear_history