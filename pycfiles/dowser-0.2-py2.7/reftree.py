# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/dowser/reftree.py
# Compiled at: 2013-08-29 04:36:04
import gc, sys
from types import FrameType

class Tree:

    def __init__(self, obj):
        self.obj = obj
        self.filename = sys._getframe().f_code.co_filename
        self._ignore = {}

    def ignore(self, *objects):
        for obj in objects:
            self._ignore[id(obj)] = None

        return

    def ignore_caller(self):
        f = sys._getframe()
        cur = f.f_back
        self.ignore(cur, cur.f_builtins, cur.f_locals, cur.f_globals)
        caller = f.f_back
        self.ignore(caller, caller.f_builtins, caller.f_locals, caller.f_globals)

    def walk(self, maxresults=100, maxdepth=None):
        """Walk the object tree, ignoring duplicates and circular refs."""
        self.seen = {}
        self.ignore(self, self.__dict__, self.obj, self.seen, self._ignore)
        self.ignore_caller()
        self.maxdepth = maxdepth
        count = 0
        for result in self._gen(self.obj):
            yield result
            count += 1
            if maxresults and count >= maxresults:
                yield (0, 0, '==== Max results reached ====')
                raise StopIteration

    def print_tree(self, maxresults=100, maxdepth=None):
        """Walk the object tree, pretty-printing each branch."""
        self.ignore_caller()
        for depth, refid, rep in self.walk(maxresults, maxdepth):
            print '%9d' % refid, ' ' * depth * 2, rep


def _repr_container(obj):
    return '%s of len %s: %r' % (type(obj).__name__, len(obj), obj)


repr_dict = _repr_container
repr_set = _repr_container
repr_list = _repr_container
repr_tuple = _repr_container

def repr_str(obj):
    return '%s of len %s: %r' % (type(obj).__name__, len(obj), obj)


repr_unicode = repr_str

def repr_frame(obj):
    return 'frame from %s line %s' % (obj.f_code.co_filename, obj.f_lineno)


def get_repr(obj, limit=250):
    typename = getattr(type(obj), '__name__', None)
    handler = globals().get('repr_%s' % typename, repr)
    try:
        result = handler(obj)
    except:
        result = 'unrepresentable object: %r' % sys.exc_info()[1]

    if len(result) > limit:
        result = result[:limit] + '...'
    return result


class ReferentTree(Tree):

    def _gen(self, obj, depth=0):
        if self.maxdepth and depth >= self.maxdepth:
            yield (
             depth, 0, '---- Max depth reached ----')
            raise StopIteration
        for ref in gc.get_referents(obj):
            if id(ref) in self._ignore:
                continue
            else:
                if id(ref) in self.seen:
                    yield (
                     depth, id(ref), '!' + get_repr(ref))
                    continue
                else:
                    self.seen[id(ref)] = None
                    yield (depth, id(ref), get_repr(ref))
                for child in self._gen(ref, depth + 1):
                    yield child

        return


class ReferrerTree(Tree):

    def _gen(self, obj, depth=0):
        if self.maxdepth and depth >= self.maxdepth:
            yield (
             depth, 0, '---- Max depth reached ----')
            raise StopIteration
        refs = gc.get_referrers(obj)
        refiter = iter(refs)
        self.ignore(refs, refiter)
        for ref in refiter:
            if isinstance(ref, FrameType):
                if ref.f_code.co_filename == self.filename:
                    continue
            if id(ref) in self._ignore:
                continue
            else:
                if id(ref) in self.seen:
                    yield (
                     depth, id(ref), '!' + get_repr(ref))
                    continue
                else:
                    self.seen[id(ref)] = None
                    yield (depth, id(ref), get_repr(ref))
                for parent in self._gen(ref, depth + 1):
                    yield parent

        return


class CircularReferents(Tree):

    def walk(self, maxresults=100, maxdepth=None):
        """Walk the object tree, showing circular referents."""
        self.stops = 0
        self.seen = {}
        self.ignore(self, self.__dict__, self.seen, self._ignore)
        self.ignore_caller()
        self.maxdepth = maxdepth
        count = 0
        for result in self._gen(self.obj):
            yield result
            count += 1
            if maxresults and count >= maxresults:
                yield (0, 0, '==== Max results reached ====')
                raise StopIteration

    def _gen(self, obj, depth=0, trail=None):
        if self.maxdepth and depth >= self.maxdepth:
            self.stops += 1
            raise StopIteration
        if trail is None:
            trail = []
        for ref in gc.get_referents(obj):
            if id(ref) in self._ignore:
                continue
            else:
                if id(ref) in self.seen:
                    continue
                else:
                    self.seen[id(ref)] = None
                refrepr = get_repr(ref)
                if id(ref) == id(self.obj):
                    yield trail + [refrepr]
                for child in self._gen(ref, depth + 1, trail + [refrepr]):
                    yield child

        return

    def print_tree(self, maxresults=100, maxdepth=None):
        """Walk the object tree, pretty-printing each branch."""
        self.ignore_caller()
        for trail in self.walk(maxresults, maxdepth):
            print trail

        if self.stops:
            print '%s paths stopped because max depth reached' % self.stops


def count_objects():
    d = {}
    for obj in gc.get_objects():
        objtype = type(obj)
        d[objtype] = d.get(objtype, 0) + 1

    d = [ (v, k) for k, v in d.iteritems() ]
    d.sort()
    return d