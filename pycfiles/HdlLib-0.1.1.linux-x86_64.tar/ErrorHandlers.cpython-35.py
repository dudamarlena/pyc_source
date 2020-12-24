# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.5/dist-packages/HdlLib/Utilities/ErrorHandlers.py
# Compiled at: 2017-07-08 08:29:58
# Size of source mod 2**32: 548 bytes
import sys, os, re, logging

class HdlLibError(Exception):

    def __init__(self, Message='HdlLib error'):
        self.Message = Message

    def __str__(self):
        return repr(self.Message)


class ParseError(HdlLibError):

    def __init__(self, Message='HdlLib error'):
        self.Message = Message
        logging.error(Message)

    def __str__(self):
        return repr(self.Message)