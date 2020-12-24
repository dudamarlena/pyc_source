# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/gman/Documents/code/Flask-Blogging/test/utils.py
# Compiled at: 2018-02-15 00:06:52
# Size of source mod 2**32: 948 bytes
import random

def get_random_unicode(length):
    try:
        get_char = unichr
    except NameError:
        get_char = chr

    include_ranges = [
     (33, 33),
     (35, 38),
     (40, 126),
     (161, 172),
     (174, 255),
     (256, 383),
     (384, 591),
     (11360, 11391),
     (5792, 5872),
     (880, 887),
     (890, 894),
     (900, 906),
     (908, 908)]
    alphabet = [get_char(code_point) for current_range in include_ranges for code_point in range(current_range[0], current_range[1] + 1)]
    return ''.join(random.choice(alphabet) for i in range(length))