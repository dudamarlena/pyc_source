# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.7/site-packages/guessit/transfo/guess_country.py
# Compiled at: 2013-03-18 16:30:48
from __future__ import unicode_literals
from guessit.country import Country
from guessit import Guess
import logging
log = logging.getLogger(__name__)
country_common_words = frozenset([b'bt', b'bb'])

def process(mtree):
    for node in mtree.unidentified_leaves():
        if len(node.node_idx) == 2:
            c = node.value[1:-1].lower()
            if c in country_common_words:
                continue
            if node.value[0] + node.value[(-1)] not in ('()', '[]', '{}'):
                continue
            try:
                country = Country(c, strict=True)
            except ValueError:
                continue

            node.guess = Guess(country=country, confidence=1.0)