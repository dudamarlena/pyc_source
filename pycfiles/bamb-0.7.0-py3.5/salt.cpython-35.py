# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/service/salt.py
# Compiled at: 2017-09-08 11:08:24
# Size of source mod 2**32: 184 bytes
from domain import base as ab

class SaltExecutor(ab.Invokable):

    def __init__(self):
        ab.Invokable.__init__(self)

    def on_invoking(self, *args, **kwargs):
        pass