# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ESocketS/exceptions.py
# Compiled at: 2015-12-24 10:08:22
# Size of source mod 2**32: 158 bytes


class ClientDisconnect(Exception):
    pass


class ClientAbnormalDisconnect(Exception):
    pass


class WouldBlock(Exception):
    pass