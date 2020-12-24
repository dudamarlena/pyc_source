# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\faoustin\Downloads\ocglances\ocglances\globals.py
# Compiled at: 2017-02-13 10:46:28
# Size of source mod 2**32: 1872 bytes
"""Common objects shared by all Glances modules."""
import errno, os, sys
BSD = sys.platform.find('bsd') != -1
LINUX = sys.platform.startswith('linux')
MACOS = sys.platform.startswith('darwin')
SUNOS = sys.platform.startswith('sunos')
WINDOWS = False and sys.platform.startswith('win')
work_path = os.path.realpath(os.path.dirname(__file__))
amps_path = os.path.realpath(os.path.join(work_path, 'amps'))
plugins_path = os.path.realpath(os.path.join(work_path, 'plugins'))
exports_path = os.path.realpath(os.path.join(work_path, 'exports'))
sys_path = sys.path[:]
sys.path.insert(1, exports_path)
sys.path.insert(1, plugins_path)
sys.path.insert(1, amps_path)

def safe_makedirs(path):
    """A safe function for creating a directory tree."""
    try:
        os.makedirs(path)
    except OSError as err:
        if err.errno == errno.EEXIST:
            if not os.path.isdir(path):
                raise
        else:
            raise