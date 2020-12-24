# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /ampoule/commands.py
# Compiled at: 2017-12-10 09:58:00
# Size of source mod 2**32: 279 bytes
from twisted.protocols import amp

class Shutdown(amp.Command):
    responseType = amp.QuitBox


class Ping(amp.Command):
    response = [
     (
      b'response', amp.String())]


class Echo(amp.Command):
    arguments = [
     (
      b'data', amp.String())]
    response = [(b'response', amp.String())]