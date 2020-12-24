# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pylinkirc/world.py
# Compiled at: 2020-04-11 03:31:40
# Size of source mod 2**32: 1425 bytes
__doc__ = '\nworld.py: Stores global variables for PyLink, including lists of active IRC objects and plugins.\n'
import threading, time
from collections import defaultdict, deque
testing = False
hooks = defaultdict(list)
networkobjects = {}
plugins = {}
services = {}
exttarget_handlers = {}
started = threading.Event()
start_ts = time.time()
shutting_down = threading.Event()
source = 'https://github.com/jlu5/PyLink'
fallback_hostname = 'pylink.int'
_log_queue = deque()
_should_remove_pid = False
daemon = False