# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.7/site-packages/guessit/transfo/guess_episode_info_from_position.py
# Compiled at: 2013-03-18 16:30:48
from __future__ import unicode_literals
from guessit.transfo import found_property
from guessit.patterns import non_episode_title, unlikely_series
import logging
log = logging.getLogger(__name__)

def match_from_epnum_position(mtree, node):
    epnum_idx = node.node_idx

    def before_epnum_in_same_pathgroup():
        return [ leaf for leaf in mtree.unidentified_leaves() if leaf.node_idx[0] == epnum_idx[0] and leaf.node_idx[1:] < epnum_idx[1:]
               ]

    def after_epnum_in_same_pathgroup():
        return [ leaf for leaf in mtree.unidentified_leaves() if leaf.node_idx[0] == epnum_idx[0] and leaf.node_idx[1:] > epnum_idx[1:]
               ]

    def after_epnum_in_same_explicitgroup():
        return [ leaf for leaf in mtree.unidentified_leaves() if leaf.node_idx[:2] == epnum_idx[:2] and leaf.node_idx[2:] > epnum_idx[2:]
               ]

    title_candidates = [ n for n in after_epnum_in_same_pathgroup() if n.clean_value.lower() not in non_episode_title
                       ]
    if b'title' not in mtree.info and before_epnum_in_same_pathgroup() == [] and len(title_candidates) == 2:
        found_property(title_candidates[0], b'series', confidence=0.4)
        found_property(title_candidates[1], b'title', confidence=0.4)
        return
    series_candidates = before_epnum_in_same_pathgroup()
    if len(series_candidates) >= 1:
        found_property(series_candidates[0], b'series', confidence=0.7)
    title_candidates = [ n for n in after_epnum_in_same_pathgroup() if n.clean_value.lower() not in non_episode_title
                       ]
    if len(title_candidates) == 1:
        found_property(title_candidates[0], b'title', confidence=0.5)
        return
    title_candidates = [ n for n in after_epnum_in_same_explicitgroup() if n.clean_value.lower() not in non_episode_title
                       ]
    if len(title_candidates) == 1:
        found_property(title_candidates[0], b'title', confidence=0.4)
        return
    if len(title_candidates) > 1:
        found_property(title_candidates[0], b'title', confidence=0.3)
        return
    title_candidates = [ n for n in after_epnum_in_same_pathgroup() if n.clean_value.lower() not in non_episode_title
                       ]
    if title_candidates:
        maxidx = -1
        maxv = -1
        for i, c in enumerate(title_candidates):
            if len(c.clean_value) > maxv:
                maxidx = i
                maxv = len(c.clean_value)

        found_property(title_candidates[maxidx], b'title', confidence=0.3)


def process(mtree):
    eps = [ node for node in mtree.leaves() if b'episodeNumber' in node.guess ]
    if eps:
        match_from_epnum_position(mtree, eps[0])
    else:
        basename = mtree.node_at((-2, ))
        title_candidates = [ n for n in basename.unidentified_leaves() if n.clean_value.lower() not in non_episode_title
                           ]
        if len(title_candidates) >= 2:
            found_property(title_candidates[0], b'series', 0.4)
            found_property(title_candidates[1], b'title', 0.4)
        else:
            if len(title_candidates) == 1:
                found_property(title_candidates[0], b'series', 0.4)
            try:
                series_candidates = mtree.node_at((-3, )).unidentified_leaves()
            except ValueError:
                series_candidates = []

        if len(series_candidates) == 1:
            found_property(series_candidates[0], b'series', 0.3)
        eps = [ node for node in mtree.nodes() if b'season' in node.guess and b'episodeNumber' not in node.guess
              ]
        if eps:
            previous = [ node for node in mtree.unidentified_leaves() if node.node_idx[0] == eps[0].node_idx[0] - 1 ]
            if len(previous) == 1:
                found_property(previous[0], b'series', 0.5)
        for node in mtree.nodes():
            if b'series' in node.guess:
                if node.guess[b'series'].lower() in unlikely_series:
                    new_confidence = node.guess.confidence(b'series') * 0.5
                    node.guess.set_confidence(b'series', new_confidence)