# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/process_tracing/constants.py
# Compiled at: 2016-11-17 08:37:26
# Size of source mod 2**32: 477 bytes
"""
Process tracing constants

Package: process_tracing
Author: Michael Witt
Mail: m.witt@htw-berlin.de
Licence: GPLv3
"""
TRACING_MODE_RUNTIME_TRACING = 1
TRACING_MODE_FILE_ACCESS = 2
TRACING_MODE_FILE_ACCESS_DETAILED = TRACING_MODE_FILE_ACCESS | 4
TRACING_MODE_SYSCALLS = 8
TRACING_MODE_SYSCALL_ARGUMENTS = TRACING_MODE_SYSCALLS | 16
TRACING_MODE_MASK = 255
TRACING_RECORD_MODE_MEMORY = 1
TRACING_RECORD_MODE_FILE = 2
TRACING_RECORD_MODE_CALLBACK = 4