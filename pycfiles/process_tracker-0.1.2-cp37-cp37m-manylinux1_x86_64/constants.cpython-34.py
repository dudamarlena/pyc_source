# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/process_tracing/constants.py
# Compiled at: 2016-11-17 08:37:26
# Size of source mod 2**32: 477 bytes
__doc__ = '\nProcess tracing constants\n\nPackage: process_tracing\nAuthor: Michael Witt\nMail: m.witt@htw-berlin.de\nLicence: GPLv3\n'
TRACING_MODE_RUNTIME_TRACING = 1
TRACING_MODE_FILE_ACCESS = 2
TRACING_MODE_FILE_ACCESS_DETAILED = TRACING_MODE_FILE_ACCESS | 4
TRACING_MODE_SYSCALLS = 8
TRACING_MODE_SYSCALL_ARGUMENTS = TRACING_MODE_SYSCALLS | 16
TRACING_MODE_MASK = 255
TRACING_RECORD_MODE_MEMORY = 1
TRACING_RECORD_MODE_FILE = 2
TRACING_RECORD_MODE_CALLBACK = 4