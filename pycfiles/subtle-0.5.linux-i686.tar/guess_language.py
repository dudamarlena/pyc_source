# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.7/site-packages/guessit/transfo/guess_language.py
# Compiled at: 2013-03-18 16:30:48
from __future__ import unicode_literals
from guessit import Guess
from guessit.transfo import SingleNodeGuesser
from guessit.language import search_language
from guessit.textutils import clean_string
import logging
log = logging.getLogger(__name__)

def guess_language(string):
    language, span, confidence = search_language(string)
    if language:
        if b'sub' in clean_string(string[:span[0]]).lower().split(b' '):
            return (
             Guess({b'subtitleLanguage': language}, confidence=confidence),
             span)
        else:
            return (
             Guess({b'language': language}, confidence=confidence),
             span)

    return (None, None)


def process(mtree):
    SingleNodeGuesser(guess_language, None, log).process(mtree)
    return