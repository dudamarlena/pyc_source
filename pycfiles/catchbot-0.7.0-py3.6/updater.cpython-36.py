# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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