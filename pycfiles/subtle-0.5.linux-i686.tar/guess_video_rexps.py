# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.7/site-packages/guessit/transfo/guess_video_rexps.py
# Compiled at: 2013-03-18 16:30:48
from __future__ import unicode_literals
from guessit import Guess
from guessit.transfo import SingleNodeGuesser
from guessit.patterns import video_rexps, sep
import re, logging
log = logging.getLogger(__name__)

def guess_video_rexps(string):
    string = b'-' + string + b'-'
    for rexp, confidence, span_adjust in video_rexps:
        match = re.search(sep + rexp + sep, string, re.IGNORECASE)
        if match:
            metadata = match.groupdict()
            if metadata.get(b'cdNumberTotal', -1) is None:
                del metadata[b'cdNumberTotal']
            return (Guess(metadata, confidence=confidence),
             (
              match.start() + span_adjust[0],
              match.end() + span_adjust[1] - 2))

    return (None, None)


def process(mtree):
    SingleNodeGuesser(guess_video_rexps, None, log).process(mtree)
    return