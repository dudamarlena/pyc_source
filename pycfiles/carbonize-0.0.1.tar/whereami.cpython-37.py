# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/lib/python3.7/site-packages/carbonium_fb/contrib/whereami.py
# Compiled at: 2019-09-02 08:45:08
# Size of source mod 2**32: 482 bytes
__doc__ = 'This module provides the WhereAmI contrib command'
from ..handlers import CommandHandler
from ..dataclasses import Message

class WhereAmICommand(CommandHandler):
    """WhereAmICommand"""

    def __init__(self, command='whereami'):
        super().__init__(handler=None, command=command)

    def handlerfn(self, message: Message, bot):
        message.reply(repr(message.thread))