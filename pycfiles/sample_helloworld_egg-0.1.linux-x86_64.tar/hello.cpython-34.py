# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/fsufitch/helloworld_egg/lib/python3.4/site-packages/helloworld/hello.py
# Compiled at: 2014-05-20 17:29:35
# Size of source mod 2**32: 137 bytes


class Hello(object):

    def __init__(self, message):
        self.message = message

    def display(self):
        print(message)