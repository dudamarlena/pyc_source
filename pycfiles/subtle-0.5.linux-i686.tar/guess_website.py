# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.7/site-packages/guessit/transfo/guess_website.py
# Compiled at: 2013-03-18 16:30:48
from __future__ import unicode_literals
from guessit.transfo import SingleNodeGuesser
from guessit.patterns import websites
import logging
log = logging.getLogger(__name__)

def guess_website(string):
    low = string.lower()
    for site in websites:
        pos = low.find(site.lower())
        if pos != -1:
            return ({b'website': site}, (pos, pos + len(site)))

    return (None, None)


def process(mtree):
    SingleNodeGuesser(guess_website, 1.0, log).process(mtree)