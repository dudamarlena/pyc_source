# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.4-fat/egg/tagger/utils.py
# Compiled at: 2006-10-04 13:57:26
from rdflib import Namespace
from datetime import datetime
from types import GeneratorType
import pdb

class nscollection(object):
    """ collection object """
    __module__ = __name__

    def bindAll(self, graph):
        for key in self.__dict__.keys():
            attr = getattr(self, key)
            if isinstance(attr, Namespace):
                graph.bind(key, attr)


def utcnow():
    now = datetime.utcnow()
    isod = now.date().isoformat()
    isot = now.time().isoformat()
    return '%sT%sUTC' % (isod, isot)


def any(i):
    return bool([ x for x in i if x ])


def all(i):
    return len([ x for x in i if x ]) == len(i)


def set_intersect(set1, set2):
    return set1 & set2


def flatten_generators(i):
    for item in i:
        if isinstance(i, GeneratorType):
            yield flatten_generators(i)
        yield i


def debug(trace=True, pm=False):

    def mkfunc(f):

        def wrap(*args, **kwargs):
            try:
                if trace:
                    pdb.set_trace()
                return f(*args, **kwargs)
            except:
                import sys
                pdb.post_mortem(sys.exc_info()[2])

        return wrap

    return mkfunc


try:
    from zope.interface import Attribute, Interface
    from zope.interface import implements
except ImportError:

    def nullfx(*args, **kwargs):
        pass


    Attribute = nullfx
    implements = nullfx

    class Interface(object):
        """how 'bout a keyword guido?"""
        __module__ = __name__