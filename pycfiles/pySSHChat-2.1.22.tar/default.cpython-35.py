# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/vlad/source/pySSHChat/pysshchat/commands/default.py
# Compiled at: 2018-04-17 04:40:28
# Size of source mod 2**32: 762 bytes
import pysshchat.variables as variables
from pysshchat.chats.commands import register
import pysshchat.chats.events as events

@register('help', 'f1')
def do_help(user, args):
    user.print_text(variables.texts.get('help', '').strip(), 'service')


@register('color', 'f2')
def do_color(user, args):
    user.change_color()


@register('me')
def do_me(cur_user, args):
    for user in variables.users.values():
        user.print_text('* %s %s' % (cur_user.username, ' '.join(args)), 'service')


@register('quit')
def do_close(user, args):
    user.quit(False)
    user.process.close()
    events.left_user(user)