# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/cblog/spamfilters/content.py
# Compiled at: 2006-12-06 04:38:00
import re
from os.path import dirname, exists, join
from turbogears import config

def read_blacklist():
    """Read a list of regular expressions."""
    blacklist = []
    blacklist_file = config.get('spam_filter.filters.content.blacklist')
    if not blacklist:
        default_bl = join(dirname(__file__), 'content_blacklist.txt')
        if exists(default_bl):
            blacklist_file = default_bl
    if blacklist_file:
        try:
            f = open(blacklist_file)
        except:
            pass
        else:
            for line in f:
                spec = line.strip().split('\t')
                if len(spec) >= 2:
                    blacklist.append((spec[0], spec[1]))
                else:
                    blacklist.append((spec[0], 1))

            f.close()
    return blacklist


blacklist = [ (re.compile(rx, re.DOTALL), score) for (rx, score) in read_blacklist() ]

def filter(value, state=None):
    scores = []
    for (rx, score) in blacklist:
        if rx.search(value.get('comment')):
            scores.append(score)

    return sum(scores)