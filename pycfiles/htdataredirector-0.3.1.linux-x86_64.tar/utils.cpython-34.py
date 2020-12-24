# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/johnny/workspaces/lazerball/src/python3.4env/lib/python3.4/site-packages/htdataredirector/utils.py
# Compiled at: 2014-10-08 05:42:38
# Size of source mod 2**32: 69 bytes
import time

def millis():
    return int(round(time.time() * 1000))