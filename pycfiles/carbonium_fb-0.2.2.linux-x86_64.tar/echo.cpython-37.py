# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.7/site-packages/carbonium_fb/contrib/echo.py
# Compiled at: 2019-09-02 08:45:08
# Size of source mod 2**32: 823 bytes
from ..handlers import CommandHandler
from ..dataclasses import Message
from .._i18n import _

class EchoCommand(CommandHandler):
    __doc__ = '\n    Echo command\n\n    This command replies to a message with its contents.\n    '

    def __init__(self, command='echo'):
        super().__init__(handler=None, command=command)

    def handlerfn(self, message: Message, bot):
        text = _('"{quote}" - {author}').format(quote=(message.args),
          author=(message.get_author_name()))
        message.reply(text)