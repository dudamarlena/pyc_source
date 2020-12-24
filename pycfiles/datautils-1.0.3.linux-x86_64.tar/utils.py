# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/graham/.virtualenvs/temcagt/lib/python2.7/site-packages/datautils/grouping/utils.py
# Compiled at: 2013-12-13 14:50:04
from continuous import ContinuousGroup
from discrete import DiscreteGroup
from .. import ddict
DefaultGroup = DiscreteGroup

def guess_type(values, key=None):
    if len(values) == 0:
        return DiscreteGroup
    else:
        v = values[0] if key is None else key(values[0])
        if isinstance(v, float):
            return ContinuousGroup
        return DiscreteGroup
        return


def lookup_gtype(gtype):
    if isinstance(gtype, str):
        if gtype in ('discrete', 'd'):
            return DiscreteGroup
        if gtype in ('continuous', 'c'):
            return ContinuousGroup
    elif gtype in (DiscreteGroup, ContinuousGroup):
        return gtype
    raise ValueError('Unknown gtype[%s]' % gtype)


def group(values, key=None, levels=None, gtype=None, gkwargs=None, dget=True):
    """

    values : list, tuple or etc...
        values to group

    key : function or None (default)
        used to 'unlock' the grouping value for each value in values

    levels : dict
        grouping levels, keys=names, values=test functions

    gtype : str, class or None (default)
        the grouping class or string to lookup class (see lookup_gtype)
        if None, gtype will be guesssed (guess_gtype)

    gkwargs : dict
        group kwargs see gtype.group

    dget : bool
        use dotted get for string keys (see ddict.ops.dget)
    """
    if len(values) == 0:
        return {}
    else:
        if isinstance(key, str):
            sv = key
            if dget:
                key = lambda x: ddict.ops.dget(x, sv)
            else:
                key = lambda x: x[sv]
        gtype = guess_type(values, key) if gtype is None else lookup_gtype(gtype)
        g = gtype(levels)
        gkwargs = {} if gkwargs is None else gkwargs
        return g(values, key=key, **gkwargs)


def group2(values, key1=None, key2=None, levels1=None, levels2=None, gtype1=None, gtype2=None, gkwargs1=None, gkwargs2=None):
    return dict([ (k, group(v, key=key2, levels=levels2, gtype=gtype2, gkwargs=gkwargs2)) for k, v in group(values, key=key1, levels=levels1, gtype=gtype1, gkwargs=gkwargs1).iteritems()
                ])


def dwalk(d):
    for k, v in d.iteritems():
        if isinstance(v, dict):
            for sk, sv in dwalk(v):
                yield (
                 (
                  k,) + sk, sv)

        else:
            yield (
             (
              k,), v)


def groupn(values, keys=None, levels=None, gtypes=None, gkwargs=None, dget=True):
    nlvls = [ len(i) for i in (keys, levels, gtypes, gkwargs) if i is not None and not isinstance(i, str) and hasattr(i, '__len__')
            ]
    if len(nlvls) == 0:
        raise ValueError('One of the following must be a list or tuple: keys, levels, gtypes, gkwargs')
    nlvls = max(nlvls)
    if not hasattr(keys, '__len__'):
        keys = [
         keys] * nlvls
    if levels is None or not hasattr(levels[0], '__len__'):
        levels = [
         levels] * nlvls
    if isinstance(gtypes, str) or not hasattr(gtypes, '__len__'):
        gtypes = [
         gtypes] * nlvls
    if gkwargs is None or isinstance(gkwargs, dict):
        gkwargs = [
         gkwargs] * nlvls
    for i in (keys, levels, gtypes, gkwargs):
        if len(i) != nlvls:
            raise ValueError('argument does not contain enough [%i] items: %s' % (
             nlvls, i))

    for i in xrange(nlvls):
        if i == 0:
            g = group(values, keys[i], levels[i], gtypes[i], gkwargs[i], dget=dget)
        else:
            for ks, vs in dwalk(g):
                reduce(dict.__getitem__, ks[:-1], g)[ks[(-1)]] = group(vs, keys[i], levels[i], gtypes[i], gkwargs[i])

    return g