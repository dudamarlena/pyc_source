# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/scripts-2.7/which.py
# Compiled at: 2017-12-15 13:22:29
import sys
from ppu.find_executable import find_executable
if len(sys.argv) != 2:
    sys.exit('Usage: %s program' % sys.argv[0])
program = find_executable(sys.argv[1])
if program:
    print program