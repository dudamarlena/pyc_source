# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pylinkirc/plugins/example.py
# Compiled at: 2020-04-11 03:31:40
# Size of source mod 2**32: 2977 bytes
import random
from pylinkirc import utils
from pylinkirc.log import log

def hook_privmsg(irc, source, command, args):
    channel = args['target']
    text = args['text']
    if irc.is_channel(channel):
        if irc.pseudoclient.nick in text:
            irc.msg(channel, 'hi there!')
            log.info('%s said my name on channel %s (PRIVMSG hook caught)' % (source, channel))


utils.add_hook(hook_privmsg, 'PRIVMSG')

def randint(irc, source, args):
    """[<min> <max>]

    Returns a random number between <min> and <max>. <min> and <max> default to 1 and 10
    respectively, if both aren't given.

    Example second paragraph here."""
    try:
        rmin = args[0]
        rmax = args[1]
    except IndexError:
        rmin, rmax = (1, 10)

    n = random.randint(rmin, rmax)
    irc.reply(str(n))


utils.add_cmd(randint, 'random', aliases=('randint', 'getrandint'))