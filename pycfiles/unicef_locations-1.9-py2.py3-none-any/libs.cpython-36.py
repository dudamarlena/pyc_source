# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jojo/workspace/locations/src/unicef_locations/libs.py
# Compiled at: 2019-04-19 21:07:17
# Size of source mod 2**32: 172 bytes
import random

def get_random_color():
    return '#%02X%02X%02X' % (
     random.randint(0, 255),
     random.randint(0, 255),
     random.randint(0, 255))