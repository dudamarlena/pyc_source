# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ialbert/web/pyblue-central/docs/context.py
# Compiled at: 2019-04-02 09:06:58
# Size of source mod 2**32: 251 bytes
NUMBERS = range(5)

def say_hello(name):
    return 'Hello %s' % name


greeting = say_hello('World!')