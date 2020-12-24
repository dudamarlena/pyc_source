# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/guyskk/anyant/weirb/src/weirb/project-template/echo/config.py
# Compiled at: 2018-06-29 08:18:43
# Size of source mod 2**32: 109 bytes
from validr import T

class Config:
    echo_times = T.int.min(1).default(1)


plugins = []
validators = {}