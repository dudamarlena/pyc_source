# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/catchbot/updater.py
# Compiled at: 2018-06-23 13:58:03
# Size of source mod 2**32: 286 bytes
import telegram.ext as tg
from .commands import commands

def create_updater(token):
    updater = tg.Updater(token=token)
    for command in commands:
        handler = tg.CommandHandler(command.__name__, command)
        updater.dispatcher.add_handler(handler)

    return updater