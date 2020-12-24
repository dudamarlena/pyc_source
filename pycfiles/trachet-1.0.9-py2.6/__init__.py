# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.4-x86_64/egg/trachet/__init__.py
# Compiled at: 2014-07-08 10:57:42
__author__ = 'Hayaki Saito (user@zuse.jp)'
__version__ = '1.0.9'
__license__ = 'GPL v3'
__doc__ = '\nThis program runs as a terminal filter process between terminals and applications.\nIt provides step-by-step debugging and formatted sequence tracing service.\nYou can watch terminal I/O sequence on realtime, and it enables you to do step-by-step execution.\n\nMost of terminal applications such as vi have single threaded UI and typically has blocking terminal I/O.\nSo trachet might be useful for both of terminal emulator developers and terminal application developers.\n'
from trachet import *