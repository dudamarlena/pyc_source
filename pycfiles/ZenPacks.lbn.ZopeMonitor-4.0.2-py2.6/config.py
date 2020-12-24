# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ZenPacks/lbn/ZopeMonitor/config.py
# Compiled at: 2012-01-15 13:23:20
from os import path
PROJECTNAME = 'ZenPacks.lbn.ZopeMonitor'
SKINS_DIR = path.join(path.dirname(__file__), 'skins')
SKINNAME = PROJECTNAME
GLOBALS = globals()
MUNIN_THREADS = ('total_threads', 'free_threads')
MUNIN_CACHE = ('total_objs', 'total_objs_memory', 'target_number')
MUNIN_ZODB = ('total_load_count', 'total_store_count', 'total_connections')
MUNIN_MEMORY = ('VmPeak', 'VmSize', 'VmLck', 'VmHWM', 'VmRSS', 'VmData', 'VmStk', 'VmExe',
                'VmLib', 'VmPTE')