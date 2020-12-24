# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\pycommunicate\util.py
# Compiled at: 2016-06-09 14:27:45
import random, string

def random_alphanumeric_string(length):
    chars = list(string.ascii_letters + string.digits + '-_?!., ')
    strin = ''
    for i in range(length):
        strin += random.choice(chars)

    return strin