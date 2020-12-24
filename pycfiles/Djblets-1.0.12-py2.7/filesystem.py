# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/djblets/util/filesystem.py
# Compiled at: 2019-06-12 01:17:17
from __future__ import unicode_literals
import os, sys

def is_exe_in_path(name):
    """Checks whether an executable is in the user's search path.

    This expects a name without any system-specific executable extension.
    It will append the proper extension as necessary. For example,
    use "myapp" and not "myapp.exe".

    This will return True if the app is in the path, or False otherwise.
    """
    if sys.platform == b'win32' and not name.endswith(b'.exe'):
        name += b'.exe'
    for dir in os.environ[b'PATH'].split(os.pathsep):
        if os.path.exists(os.path.join(dir, name)):
            return True

    return False