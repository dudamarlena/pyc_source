# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/graham/.virtualenvs/temcagt/lib/python2.7/site-packages/datautils/mongo/io.py
# Compiled at: 2013-12-13 14:50:04
import cPickle as pickle, numpy, pymongo
try:
    import pymongo.binary as binary
except ImportError:
    import bson.binary as binary

from .. import ddict

def write(d, pchar=','):
    """
    Some 'inspiration' (e.g. liberal copying) from:
        https://github.com/jaberg/hyperopt/blob/master/hyperopt/base.py
        SONify
    """
    if isinstance(d, dict):
        nd = {}
        for k in d.keys():
            nk = str(k)
            nk = nk.replace('.', pchar)
            nd[nk] = write(d[k])

        return nd
    if isinstance(d, (list, tuple)):
        return type(d)([ write(i) for i in d ])
    if isinstance(d, numpy.ndarray):
        if d.dtype.isbuiltin == 0:
            return binary.Binary(pickle.dumps(d, protocol=2))
        if d.dtype.isbuiltin == 1:
            return write(list(d))
        raise TypeError('Invalid numpy.ndarray dtype: %s' % d.dtype)
    else:
        if isinstance(d, numpy.bool_):
            return bool(d)
        if isinstance(d, numpy.integer):
            return int(d)
        if isinstance(d, numpy.floating):
            return float(d)
        if isinstance(d, numpy.void):
            return dict([ (k.replace('.', pchar), write(d[k])) for k in d.dtype.names
                        ])
        if isinstance(d, Exception):
            return str(d)
    return d


def read(d, dclass=ddict.DDict):
    """
    By default returns DDicts rather than dicts
    """
    if isinstance(d, dict):
        return dclass([ (k, read(v)) for k, v in d.iteritems() ])
    if isinstance(d, (list, tuple)):
        return type(d)([ read(v) for v in d ])
    if isinstance(d, binary.Binary):
        return pickle.loads(d)
    return d