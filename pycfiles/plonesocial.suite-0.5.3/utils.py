# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/gyst/plonesocial.buildout/src/plonesocial.microblog/plonesocial/microblog/utils.py
# Compiled at: 2014-01-17 08:56:06
import time
from BTrees import LLBTree
from .interfaces import IMicroblogContext

def get_microblog_context(context):
    if context is None:
        return
    else:
        if IMicroblogContext.providedBy(context):
            return context
        try:
            chain = context.aq_inner.aq_chain
        except AttributeError:
            return

        for item in chain:
            if IMicroblogContext.providedBy(item):
                return item
        else:
            return

        return


def longkeysortreverse(btreeish, minv=None, maxv=None, limit=None):
    """Performance optimized keyspace accessor.
    Returns an iterable of btreeish keys, reverse sorted by key.
    Expects a btreeish with long(microsec) keys.
    """
    try:
        accessor = btreeish.keys
    except AttributeError:
        accessor = LLBTree.TreeSet(btreeish).keys

    i = 0
    if minv or maxv:
        keys = [ x for x in accessor(min=minv, max=maxv) ]
        keys.sort()
        keys.reverse()
        for key in keys:
            yield key
            i += 1
            if i == limit:
                return

    else:
        tmax = long(time.time() * 1000000.0)
        tmin = long(tmax - 3600000000.0)
        keys = [ x for x in accessor(min=tmin, max=tmax) ]
        keys.sort()
        keys.reverse()
        for key in keys:
            yield key
            i += 1
            if i == limit:
                return

        tmax = tmin
        tmin = long(tmax - 82800000000.0)
        keys = [ x for x in accessor(min=tmin, max=tmax) ]
        keys.sort()
        keys.reverse()
        for key in keys:
            yield key
            i += 1
            if i == limit:
                return

        tmax = tmin
        keys = [ x for x in accessor(max=tmax) ]
        keys.sort()
        keys.reverse()
        for key in keys:
            yield key
            i += 1
            if i == limit:
                return