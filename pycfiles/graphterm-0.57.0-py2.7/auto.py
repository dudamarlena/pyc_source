# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-x86_64/egg/graphterm/bin/tornado/platform/auto.py
# Compiled at: 2012-01-23 14:09:34
"""Implementation of platform-specific functionality.

For each function or class described in `tornado.platform.interface`,
the appropriate platform-specific implementation exists in this module.
Most code that needs access to this functionality should do e.g.::

    from tornado.platform.auto import set_close_exec
"""
import os
if os.name == 'nt':
    from tornado.platform.windows import set_close_exec, Waker
else:
    from tornado.platform.posix import set_close_exec, Waker