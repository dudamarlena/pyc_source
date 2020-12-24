# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.7/site-packages/guessit/transfo/guess_bonus_features.py
# Compiled at: 2013-03-18 16:30:48
from __future__ import unicode_literals
from guessit.transfo import found_property
import logging
log = logging.getLogger(__name__)

def process(mtree):

    def previous_group(g):
        for leaf in mtree.unidentified_leaves()[::-1]:
            if leaf.node_idx < g.node_idx:
                return leaf

    def next_group(g):
        for leaf in mtree.unidentified_leaves():
            if leaf.node_idx > g.node_idx:
                return leaf

    def same_group(g1, g2):
        return g1.node_idx[:2] == g2.node_idx[:2]

    bonus = [ node for node in mtree.leaves() if b'bonusNumber' in node.guess ]
    if bonus:
        bonusTitle = next_group(bonus[0])
        if same_group(bonusTitle, bonus[0]):
            found_property(bonusTitle, b'bonusTitle', 0.8)
    filmNumber = [ node for node in mtree.leaves() if b'filmNumber' in node.guess ]
    if filmNumber:
        filmSeries = previous_group(filmNumber[0])
        found_property(filmSeries, b'filmSeries', 0.9)
        title = next_group(filmNumber[0])
        found_property(title, b'title', 0.9)
    season = [ node for node in mtree.leaves() if b'season' in node.guess ]
    if season and b'bonusNumber' in mtree.info:
        series = previous_group(season[0])
        if same_group(series, season[0]):
            found_property(series, b'series', 0.9)