# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.7/site-packages/carbonium_fb/contrib/whereami.py
# Compiled at: 2019-09-02 08:45:08
# Size of source mod 2**32: 482 bytes
"""This module provides the WhereAmI contrib command"""
from ..handlers import CommandHandler
from ..dataclasses import Message

class WhereAmICommand(CommandHandler):
    __doc__ = '\n    "whereami" command\n\n    This command replies to a message with\n    the thread it was received from.\n    '

    def __init__(self, command='whereami'):
        super().__init__(handler=None, command=command)

    def handlerfn(self, message: Message, bot):
        message.reply(repr(message.thread))