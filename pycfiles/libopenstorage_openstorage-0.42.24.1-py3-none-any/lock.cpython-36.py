# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-ed191__6/cffi/cffi/lock.py
# Compiled at: 2020-01-10 16:25:38
# Size of source mod 2**32: 747 bytes
import sys
if sys.version_info < (3, ):
    try:
        from thread import allocate_lock
    except ImportError:
        from dummy_thread import allocate_lock

try:
    from _thread import allocate_lock
except ImportError:
    from _dummy_thread import allocate_lock