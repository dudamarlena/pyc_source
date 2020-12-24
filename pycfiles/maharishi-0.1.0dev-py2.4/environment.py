# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/maharishi/config/environment.py
# Compiled at: 2006-08-30 12:30:23
import os, pylons.config
from maharishi.config.routing import make_map

def load_environment():
    map = make_map()
    root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    paths = {'root_path': root_path, 'controllers': os.path.join(root_path, 'controllers'), 'templates': [ os.path.join(root_path, path) for path in ('components', 'templates') ], 'static_files': os.path.join(root_path, 'public')}
    myghty = {}
    myghty['log_errors'] = True
    return pylons.config.Config(myghty, map, paths)