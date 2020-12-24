# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./src/assets/version.py
# Compiled at: 2020-01-01 14:22:44
# Size of source mod 2**32: 221 bytes
from pathlib import Path
ROOT = Path(__file__).parent.parent
with open(str(ROOT / 'VERSION'), 'r') as (f):
    version = f.read().strip()

def get_value():
    return version