# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/cleanco/clean.py
# Compiled at: 2020-04-26 10:23:49
# Size of source mod 2**32: 2896 bytes
__doc__ = 'Functions to help clean & normalize business names.\n\nSee http://www.unicode.org/reports/tr15/#Normalization_Forms_Table for details\non Unicode normalization and the NFKD normalization used here.\n\nBasic usage:\n\n>> terms = prepare_terms()\n>> basename("Daddy & Sons, Ltd.", terms, prefix=True, middle=True, suffix=True)\nDaddy & Sons\n\n'
import functools, operator
from collections import OrderedDict
import re, unicodedata
from .termdata import terms_by_type, terms_by_country
tail_removal_rexp = re.compile('[^\\.\\w]+$', flags=(re.UNICODE))

def get_unique_terms():
    """retrieve all unique terms from termdata definitions"""
    ts = functools.reduce(operator.iconcat, terms_by_type.values(), [])
    cs = functools.reduce(operator.iconcat, terms_by_country.values(), [])
    return set(ts + cs)


def normalize_terms(terms):
    """normalize terms"""
    return (unicodedata.normalize('NFKD', t.casefold()) for t in terms)


def strip_tail(name):
    """get rid of all trailing non-letter symbols except the dot"""
    match = re.search(tail_removal_rexp, name)
    if match is not None:
        name = name[:match.span()[0]]
    return name


def normalized(text):
    """caseless Unicode normalization"""
    return unicodedata.normalize('NFKD', text.casefold())


def prepare_terms():
    """construct an optimized term structure for basename extraction"""
    terms = get_unique_terms()
    nterms = normalize_terms(terms)
    ntermparts = (t.split() for t in nterms)
    sntermparts = sorted(ntermparts, key=len, reverse=True)
    return [(len(tp), tp) for tp in sntermparts]


def basename(name, terms, suffix=True, prefix=False, middle=False, **kwargs):
    """return cleaned base version of the business name"""
    name = strip_tail(name)
    nparts = name.split()
    nname = normalized(name)
    nnparts = nname.split()
    nnsize = len(nnparts)
    if suffix:
        for termsize, termparts in terms:
            if nnparts[-termsize:] == termparts:
                del nnparts[-termsize:]
                del nparts[-termsize:]

    if prefix:
        for termsize, termparts in terms:
            if nnparts[:termsize] == termparts:
                del nnparts[:termsize]
                del nparts[:termsize]

    if middle:
        for termsize, termparts in terms:
            if termsize > 1:
                sizediff = nnsize - termsize
                if sizediff > 1 and termparts == ['as.', 'oy']:
                    for i in range(0, nnsize - termsize + 1):
                        if termparts == nnparts[i:i + termsize]:
                            del nnparts[i:i + termsize]
                            del nparts[i:i + termsize]

            elif termparts[0] in nnparts[1:-1]:
                idx = nnparts[1:-1].index(termparts[0])
                del nnparts[idx + 1]
                del nparts[idx + 1]

    return strip_tail(' '.join(nparts))