# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\pycommunicate\util.py
# Compiled at: 2016-06-09 14:27:45
import random, string

def random_alphanumeric_string(length):
    chars = list(string.ascii_letters + string.digits + '-_?!., ')
    strin = ''
    for i in range(length):
        strin += random.choice(chars)

    return strin