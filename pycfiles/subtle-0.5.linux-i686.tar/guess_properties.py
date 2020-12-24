# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.7/site-packages/guessit/transfo/guess_properties.py
# Compiled at: 2013-03-18 16:30:48
from __future__ import unicode_literals
from guessit.transfo import SingleNodeGuesser
from guessit.patterns import find_properties
import logging
log = logging.getLogger(__name__)

def guess_properties(string):
    try:
        prop, value, pos, end = find_properties(string)[0]
        return ({prop: value}, (pos, end))
    except IndexError:
        return (None, None)

    return


def process(mtree):
    SingleNodeGuesser(guess_properties, 1.0, log).process(mtree)