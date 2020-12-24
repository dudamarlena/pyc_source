# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.7/site-packages/guessit/transfo/guess_episodes_rexps.py
# Compiled at: 2013-03-18 16:30:48
from __future__ import unicode_literals
from guessit import Guess
from guessit.transfo import SingleNodeGuesser
from guessit.patterns import episode_rexps
import re, logging
log = logging.getLogger(__name__)

def number_list(s):
    return list(re.sub(b'[^0-9]+', b' ', s).split())


def guess_episodes_rexps(string):
    for rexp, confidence, span_adjust in episode_rexps:
        match = re.search(rexp, string, re.IGNORECASE)
        if match:
            guess = Guess(match.groupdict(), confidence=confidence)
            span = (match.start() + span_adjust[0],
             match.end() + span_adjust[1])
            if int(guess.get(b'season', 0)) > 25:
                continue
            if guess.get(b'episodeNumber'):
                eplist = number_list(guess[b'episodeNumber'])
                guess.set(b'episodeNumber', int(eplist[0]), confidence=confidence)
                if len(eplist) > 1:
                    guess.set(b'episodeList', list(map(int, eplist)), confidence=confidence)
            if guess.get(b'bonusNumber'):
                eplist = number_list(guess[b'bonusNumber'])
                guess.set(b'bonusNumber', int(eplist[0]), confidence=confidence)
            return (
             guess, span)

    return (None, None)


def process(mtree):
    SingleNodeGuesser(guess_episodes_rexps, None, log).process(mtree)
    return