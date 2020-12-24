# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/boyhack/programs/pocsuite3/pocsuite3/lib/request/patch/remove_warnings.py
# Compiled at: 2019-03-15 03:35:12
# Size of source mod 2**32: 58 bytes
from urllib3 import disable_warnings
disable_warnings()