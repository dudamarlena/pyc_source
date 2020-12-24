# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /ampoule/commands.py
# Compiled at: 2017-12-10 09:58:00
# Size of source mod 2**32: 279 bytes
from twisted.protocols import amp

class Shutdown(amp.Command):
    responseType = amp.QuitBox


class Ping(amp.Command):
    response = [
     (
      'response', amp.String())]


class Echo(amp.Command):
    arguments = [
     (
      'data', amp.String())]
    response = [('response', amp.String())]