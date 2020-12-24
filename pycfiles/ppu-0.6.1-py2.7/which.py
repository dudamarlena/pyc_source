# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/scripts-2.7/which.py
# Compiled at: 2017-12-15 13:22:29
import sys
from ppu.find_executable import find_executable
if len(sys.argv) != 2:
    sys.exit('Usage: %s program' % sys.argv[0])
program = find_executable(sys.argv[1])
if program:
    print program