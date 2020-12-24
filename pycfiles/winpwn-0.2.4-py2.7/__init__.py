# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\winpwn\__init__.py
# Compiled at: 2020-04-17 05:14:22
import os, sys
cwd = os.path.dirname(__file__)
sys.path = [cwd] + sys.path[1:]
from .context import context
from .winpwn import process, remote
from .dbg import gdb, windbg, x64dbg, windbgx, init_debugger
from .misc import p8, p16, p32, p64, u8, u16, u32, u64, pause, sleep, NOPIE, PIE, Latin1_encode, Latin1_decode, color, hexdump
from .asm import asm, disasm
from .winfile import winfile
from .wincs import wincs
init_debugger()
tostr = Latin1_decode
tobyte = Latin1_encode
__all__ = [
 'process', 'remote', 'gdb', 'windbg', 'x64dbg', 'windbgx',
 'context',
 'p8', 'p16', 'p32', 'p64', 'u8', 'u16', 'u32', 'u64',
 'pause', 'sleep', 'hexdump', 'color', 'NOPIE', 'PIE',
 'tostr', 'tobyte',
 'asm', 'disasm',
 'winfile',
 'wincs']