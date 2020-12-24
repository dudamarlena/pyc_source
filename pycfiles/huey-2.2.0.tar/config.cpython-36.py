# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/charles/code/huey/examples/simple/config.py
# Compiled at: 2018-12-11 21:58:15
# Size of source mod 2**32: 75 bytes
from huey import RedisHuey
huey = RedisHuey('simple.test', blocking=True)