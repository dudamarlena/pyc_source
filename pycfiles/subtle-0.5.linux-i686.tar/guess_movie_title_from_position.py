# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.7/site-packages/guessit/transfo/guess_movie_title_from_position.py
# Compiled at: 2013-03-18 16:30:48
from __future__ import unicode_literals
from guessit import Guess
import logging
log = logging.getLogger(__name__)

def process(mtree):

    def found_property(node, name, value, confidence):
        node.guess = Guess({name: value}, confidence=confidence)
        log.debug(b'Found with confidence %.2f: %s' % (confidence, node.guess))

    def found_title(node, confidence):
        found_property(node, b'title', node.clean_value, confidence)

    basename = mtree.node_at((-2, ))
    all_valid = lambda leaf: len(leaf.clean_value) > 0
    basename_leftover = basename.unidentified_leaves(valid=all_valid)
    try:
        folder = mtree.node_at((-3, ))
        folder_leftover = folder.unidentified_leaves()
    except ValueError:
        folder = None
        folder_leftover = []

    log.debug(b'folder: %s' % folder_leftover)
    log.debug(b'basename: %s' % basename_leftover)
    if folder_leftover and basename_leftover and folder_leftover[0].clean_value == basename_leftover[0].clean_value:
        found_title(folder_leftover[0], confidence=0.8)
        return
    else:
        try:
            series = folder_leftover[0]
            filmNumber = basename_leftover[0]
            title = basename_leftover[1]
            basename_leaves = basename.leaves()
            num = int(filmNumber.clean_value)
            log.debug(b'series: %s' % series.clean_value)
            log.debug(b'title: %s' % title.clean_value)
            if series.clean_value != title.clean_value and series.clean_value != filmNumber.clean_value and basename_leaves.index(filmNumber) == 0 and basename_leaves.index(title) == 1:
                found_title(title, confidence=0.6)
                found_property(series, b'filmSeries', series.clean_value, confidence=0.6)
                found_property(filmNumber, b'filmNumber', num, confidence=0.6)
            return
        except Exception:
            pass

        try:
            if mtree.node_at((-4, 0)).value.lower() == b'movies':
                folder = mtree.node_at((-3, ))
                year_group = folder.first_leaf_containing(b'year')
                groups_before = folder.previous_unidentified_leaves(year_group)
                found_title(groups_before[0], confidence=0.8)
                return
        except Exception:
            pass

        try:
            props = mtree.previous_leaves_containing(mtree.children[(-2)], [
             b'videoCodec', b'format',
             b'language'])
        except IndexError:
            props = []

        if props:
            group_idx = props[0].node_idx[0]
            if all(g.node_idx[0] == group_idx for g in props):
                leftover = mtree.node_at((group_idx,)).unidentified_leaves()
                if leftover:
                    found_title(leftover[0], confidence=0.7)
                    return
        if basename_leftover:
            title_candidate = basename_leftover[0]
            if title_candidate.clean_value.count(b' ') == 0 and folder_leftover and folder_leftover[0].clean_value.count(b' ') >= 2:
                found_title(folder_leftover[0], confidence=0.7)
                return
            if len(basename_leftover) == 2 and basename_leftover[0].is_explicit():
                found_title(basename_leftover[1], confidence=0.8)
                return
            found_title(title_candidate, confidence=0.6)
            return
        if folder_leftover:
            found_title(folder_leftover[0], confidence=0.5)
            return
        basename = mtree.node_at((-2, ))
        basename_leftover = basename.unidentified_leaves(valid=lambda leaf: True)
        if basename_leftover:
            found_title(basename_leftover[0], confidence=0.4)
            return
        return