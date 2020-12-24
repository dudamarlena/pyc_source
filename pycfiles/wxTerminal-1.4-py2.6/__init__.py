# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/wxTerminal/__init__.py
# Compiled at: 2013-01-24 04:21:57
__all__ = [
 'wxTerminal', 'version', 'wxTerminalMP']
from wxTerminal import *
try:
    from version import __version__
except ImportError:
    __version__ = 'Unknown'