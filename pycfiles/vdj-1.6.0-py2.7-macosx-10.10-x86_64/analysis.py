# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/vdj/analysis.py
# Compiled at: 2014-12-16 17:37:19
import itertools, numpy as np, pyutils, vdj

def iterator2countdict(iterable, features, count='read'):
    counts = pyutils.nesteddict()
    uniq_feature_values = dict([ (f, set()) for f in features ])
    for chain in iterable:
        try:
            feature_list = [ chain.__getattribute__(f) for f in features ]
            for feature, value in zip(features, feature_list):
                uniq_feature_values[feature].add(value)

        except AttributeError:
            continue

        if count == 'read':
            counts.nested_increment(feature_list)
        elif count in ('junction', 'clone'):
            counts.nested_add(feature_list, chain.__getattribute__(count))
        else:
            raise ValueError, "'count' must be 'read', 'junction', or 'clone'"

    if count in ('junction', 'clone'):
        for tup in counts.walk():
            keylist, val = tup[:-1], tup[(-1)]
            counts.nested_assign(keylist, len(val))

    counts.lock()
    for feature in features:
        uniq_feature_values[feature] = list(uniq_feature_values[feature])

    return (
     uniq_feature_values, counts)


def imgt2countdict(inhandle, features, count='read'):
    return iterator2countdict(vdj.parse_imgt(inhandle), features, count)


def countdict2matrix(features, feature_values, countdict):
    dim = tuple([ len(feature_values[f]) for f in features ])
    matrix = np.zeros(dim, dtype=np.int)
    for posvals in itertools.product(*[ list(enumerate(feature_values[f])) for f in features ]):
        pos, vals = zip(*posvals)
        count = countdict
        for val in vals:
            try:
                count = count[val]
            except KeyError:
                count = 0
                break

        matrix[pos] = count

    return matrix


def barcode_clone_counts(inhandle):
    """Return count dict from vdjxml file with counts[barcode][clone]"""
    counts = dict()
    for chain in vdj.parse_VDJXML(inhandle):
        try:
            counts_barcode = counts.setdefault(chain.barcode, dict())
        except AttributeError:
            continue

        counts_barcode[chain.clone] = counts_barcode.get(chain.clone, 0) + 1

    return counts


def barcode_junction_counts(inhandle):
    """Return count dict from vdjxml file with counts[barcode][junction]"""
    counts = dict()
    for chain in vdj.parse_VDJXML(inhandle):
        try:
            counts_barcode = counts.setdefault(chain.barcode, dict())
        except AttributeError:
            continue

        counts_barcode[chain.junction] = counts_barcode.get(chain.junction, 0) + 1

    return counts


def barcode_clone_counts2matrix(counts, barcodes=None, clones=None):
    """Generates matrix from count dict"""
    if barcodes == None:
        barcodes = counts.keys()
    if clones == None:
        clones = list(reduce(lambda x, y: x | y, [ set(c.keys()) for c in counts.itervalues() ]))
    matrix = np.zeros((len(clones), len(barcodes)))
    for col, barcode in enumerate(barcodes):
        for row, clone in enumerate(clones):
            matrix[(row, col)] = counts.get(barcode, dict()).get(clone, 0)

    return (
     clones, barcodes, matrix)


barcode_junction_counts2matrix = barcode_clone_counts2matrix