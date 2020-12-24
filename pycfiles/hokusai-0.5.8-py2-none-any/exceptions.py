# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: hokusai/lib/exceptions.py
# Compiled at: 2018-08-08 18:48:16
from subprocess import CalledProcessError

class HokusaiError(Exception):

    def __init__(self, message, return_code=1):
        self.message = message
        self.return_code = return_code