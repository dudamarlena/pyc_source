# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.7/site-packages/guessit/transfo/post_process.py
# Compiled at: 2013-03-18 16:30:48
from __future__ import unicode_literals
from guessit.patterns import subtitle_exts
from guessit.textutils import reorder_title
import logging
log = logging.getLogger(__name__)

def process(mtree):
    for node in mtree.nodes():
        if b'language' not in node.guess:
            continue

        def promote_subtitle():
            node.guess.set(b'subtitleLanguage', node.guess[b'language'], confidence=node.guess.confidence(b'language'))
            del node.guess[b'language']

        if mtree.node_at((-1, )).value.lower() in subtitle_exts and node == mtree.leaves()[(-2)]:
            promote_subtitle()
        try:
            idx = node.node_idx
            previous = mtree.node_at((idx[0], idx[1] - 1)).leaves()[(-1)]
            if previous.value.lower()[-2:] == b'st':
                promote_subtitle()
        except IndexError:
            pass

    for node in mtree.nodes():
        if b'series' not in node.guess:
            continue
        node.guess[b'series'] = reorder_title(node.guess[b'series'])