# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/ialbert/web/pyblue-central/docs/context.py
# Compiled at: 2019-04-02 09:06:58
# Size of source mod 2**32: 251 bytes
NUMBERS = range(5)

def say_hello(name):
    return 'Hello %s' % name


greeting = say_hello('World!')