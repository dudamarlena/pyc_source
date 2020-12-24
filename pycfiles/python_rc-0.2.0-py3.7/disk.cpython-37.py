# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/rc/disk.py
# Compiled at: 2020-04-21 15:20:40
# Size of source mod 2**32: 175 bytes


class Disk:

    def __init__(self, name, *, provider, size, type):
        self.name = name
        self.provider = provider
        self.size = size
        self.type = type