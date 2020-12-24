# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/afshari9978/Projects/parkners_new/avishan/__init__.py
# Compiled at: 2020-03-14 14:37:39
# Size of source mod 2**32: 139 bytes
import threading
thread_storage = threading.local()
thread_storage.current_request = {}
current_request = thread_storage.current_request