# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.7/site-packages/guessit/transfo/split_on_dash.py
# Compiled at: 2013-03-18 16:30:48
from __future__ import unicode_literals
from guessit.patterns import sep
import re, logging
log = logging.getLogger(__name__)

def process(mtree):
    for node in mtree.unidentified_leaves():
        indices = []
        didx = 0
        pattern = re.compile(sep + b'-' + sep)
        match = pattern.search(node.value)
        while match:
            span = match.span()
            indices.extend([span[0], span[1]])
            match = pattern.search(node.value, span[1])

        if indices:
            node.partition(indices)