# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.7/site-packages/guessit/transfo/guess_weak_episodes_rexps.py
# Compiled at: 2013-03-18 16:30:48
from __future__ import unicode_literals
from guessit import Guess
from guessit.transfo import SingleNodeGuesser
from guessit.patterns import weak_episode_rexps
import re, logging
log = logging.getLogger(__name__)

def guess_weak_episodes_rexps(string, node):
    if b'episodeNumber' in node.root.info:
        return (None, None)
    else:
        for rexp, span_adjust in weak_episode_rexps:
            match = re.search(rexp, string, re.IGNORECASE)
            if match:
                metadata = match.groupdict()
                span = (match.start() + span_adjust[0],
                 match.end() + span_adjust[1])
                epnum = int(metadata[b'episodeNumber'])
                if epnum > 100:
                    season, epnum = epnum // 100, epnum % 100
                    if season > 25:
                        continue
                    return (
                     Guess({b'season': season, b'episodeNumber': epnum}, confidence=0.6), span)
                return (Guess(metadata, confidence=0.3), span)

        return (None, None)


guess_weak_episodes_rexps.use_node = True

def process(mtree):
    SingleNodeGuesser(guess_weak_episodes_rexps, 0.6, log).process(mtree)