# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/breno/Envs/djangoplus/lib/python3.7/site-packages/djangoplus/__init__.py
# Compiled at: 2019-04-02 21:49:06
# Size of source mod 2**32: 125 bytes
count = 0

def next_number():
    global count
    if count > 1000:
        count = 0
    count = count + 1
    return count