# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/nephele/SilentException.py
# Compiled at: 2017-02-16 11:26:59


class SilentException(Exception):

    def __init__(self):
        Exception.__init__(self)