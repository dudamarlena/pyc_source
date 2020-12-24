# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/qtalchemy/xplatform/util.py
# Compiled at: 2014-02-03 12:53:12
"""
For the most part, we have functions here which do something for windows 
and something else for everything else.
"""

def is_windows():
    """
    returns True if running on windows
    """
    import sys
    return sys.platform in ('win32', 'cygwin')


def xdg_open(file):
    """
    Be a platform smart incarnation of xdg-open and open files in the correct 
    application.
    """
    import os
    if is_windows():
        try:
            import win32api
            win32api.ShellExecute(0, None, file, None, None, 1)
        except ImportError as e:
            os.system(('start {0}').format(file))

    else:
        os.system(('xdg-open {0}').format(file.replace(';', '\\;').replace('&', '\\&')))
    return