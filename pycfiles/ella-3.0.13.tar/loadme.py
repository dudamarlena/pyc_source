# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/xaralis/Workspace/elladev/ella/test_ella/test_app/loadme.py
# Compiled at: 2013-07-03 05:00:55
from ella.utils.installedapps import app_modules_loaded
run_log = []

def handle_stuff(*args, **kwargs):
    run_log.append((args, kwargs))


app_modules_loaded.connect(handle_stuff)