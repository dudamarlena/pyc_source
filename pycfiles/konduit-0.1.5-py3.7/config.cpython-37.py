# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\konduit\config.py
# Compiled at: 2019-11-18 20:04:24
# Size of source mod 2**32: 234 bytes
import os
USER_PATH = os.path.expanduser('~')
KONDUIT_BASE_DIR = os.path.join(USER_PATH, '.konduit')
KONDUIT_DIR = os.path.join(KONDUIT_BASE_DIR, 'konduit-serving')
KONDUIT_PID_STORAGE = os.path.join(KONDUIT_DIR, 'pid.json')