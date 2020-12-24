# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/xaralis/Workspace/elladev/ella/test_ella/test_utils/test_installedapps.py
# Compiled at: 2013-07-03 05:00:55
import sys
from ella.utils.installedapps import call_modules, app_modules_loaded
from nose import tools

def test_module_loaded_and_signal_fired():
    call_modules(('loadme', ))
    tools.assert_true('test_ella.test_app.loadme' in sys.modules)
    loadme = sys.modules['test_ella.test_app.loadme']
    tools.assert_equals(1, len(loadme.run_log))
    tools.assert_equals(((), {'signal': app_modules_loaded, 'sender': None}), loadme.run_log[0])
    return