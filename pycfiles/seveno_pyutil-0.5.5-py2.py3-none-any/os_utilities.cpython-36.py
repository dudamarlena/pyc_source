# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/tomislav/dev/seveno_pyutil/build/lib/seveno_pyutil/os_utilities.py
# Compiled at: 2017-10-23 05:03:29
# Size of source mod 2**32: 533 bytes
import os, pwd

def current_user_home():
    """Queries OS for path to current user home directory."""
    return pwd.getpwuid(os.getuid()).pw_dir


def current_user():
    """Queries OS for current user username."""
    return pwd.getpwuid(os.getuid()).pw_name