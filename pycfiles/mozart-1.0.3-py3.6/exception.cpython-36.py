# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/mozart/music/exception.py
# Compiled at: 2019-04-22 03:20:27
# Size of source mod 2**32: 196 bytes


class MusicIDInvalid(Exception):
    pass


class MusicDoesnotExists(Exception):
    pass


class MusicNotFound(Exception):
    pass


class MusicInfoObtainFail(Exception):
    pass