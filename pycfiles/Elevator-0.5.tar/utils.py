# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/oleiade/Dev/Sandbox/Python/Elevator/tests/utils.py
# Compiled at: 2012-10-23 04:08:00
import os, re

def rm_from_pattern(dir, pattern):
    """Removes directory files matching with a provided
    pattern"""
    for f in os.listdir(dir):
        if re.search(pattern, f):
            os.remove(os.path.join(dir, f))