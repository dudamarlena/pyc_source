# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pylinkirc/plugins/games.py
# Compiled at: 2020-04-11 03:31:40
# Size of source mod 2**32: 2343 bytes
"""
games.py: Creates a bot providing a few simple games.
"""
import random
from pylinkirc import utils
from pylinkirc.log import log
mydesc = 'The \x02Games\x02 plugin provides simple games for IRC.'
gameclient = utils.register_service('Games', default_nick='Games', manipulatable=True, desc=mydesc)
reply = gameclient.reply
error = gameclient.error

def dice(irc, source, args):
    """<num>d<sides>

    Rolls a die with <sides> sides <num> times.
    """
    if not args:
        reply(irc, 'No string given.')
        return
    try:
        num, sides = map(int, args[0].split('d', 1))
    except ValueError:
        gameclient.help(irc, source, ['dice'])
        return
    else:
        if not 1 < sides <= 100:
            raise AssertionError('Invalid side count (must be 2-100).')
        elif not 1 <= num <= 100:
            raise AssertionError('Cannot roll more than 100 dice at once.')
        results = []
        for _ in range(num):
            results.append(random.randint(1, sides))

        s = 'You rolled %s: %s (total: %s)' % (args[0], ' '.join([str(x) for x in results]), sum(results))
        reply(irc, s)


gameclient.add_cmd(dice, aliases='d', featured=True)
eightball_responses = [
 'It is certain.',
 'It is decidedly so.',
 'Without a doubt.',
 'Yes, definitely.',
 'You may rely on it.',
 'As I see it, yes.',
 'Most likely.',
 'Outlook good.',
 'Yes.',
 'Signs point to yes.',
 'Reply hazy, try again.',
 'Ask again later.',
 'Better not tell you now.',
 'Cannot predict now.',
 'Concentrate and ask again.',
 "Don't count on it.",
 'My reply is no.',
 'My sources say no.',
 'Outlook not so good.',
 'Very doubtful.']

def eightball(irc, source, args):
    """[<question>]

    Asks the Magic 8-ball a question.
    """
    reply(irc, random.choice(eightball_responses))


gameclient.add_cmd(eightball, featured=True, aliases=('8ball', '8b'))

def die(irc=None):
    utils.unregister_service('games')