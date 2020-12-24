# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /ClusterShell/RangeSet.py
# Compiled at: 2019-12-07 15:34:33
# Size of source mod 2**32: 52447 bytes
"""
Cluster range set module.

Instances of RangeSet provide similar operations than the builtin set type,
extended to support cluster ranges-like format and stepping support ("0-8/2").
"""
from functools import reduce
from itertools import product
from operator import mul
__all__ = [
 'RangeSetException',
 'RangeSetParseError',
 'RangeSetPaddingError',
 'RangeSet',
 'RangeSetND',
 'AUTOSTEP_DISABLED']
AUTOSTEP_DISABLED = 1e+100

class RangeSetException(Exception):
    __doc__ = 'Base RangeSet exception class.'


class RangeSetParseError(RangeSetException):
    __doc__ = 'Raised when RangeSet parsing cannot be done properly.'

    def __init__(self, part, msg):
        if part:
            msg = '%s : "%s"' % (msg, part)
        RangeSetException.__init__(self, msg)
        self.part = part


class RangeSetPaddingError(RangeSetParseError):
    __doc__ = 'Raised when a fatal padding incoherence occurs'

    def __init__(self, part, msg):
        RangeSetParseError.__init__(self, part, 'padding mismatch (%s)' % msg)


class RangeSet(set):
    __doc__ = '\n    Mutable set of cluster node indexes featuring a fast range-based API.\n\n    This class aims to ease the management of potentially large cluster range\n    sets and is used by the :class:`.NodeSet` class.\n\n    RangeSet basic constructors:\n\n       >>> rset = RangeSet()            # empty RangeSet\n       >>> rset = RangeSet("5,10-42")   # contains 5, 10 to 42\n       >>> rset = RangeSet("0-10/2")    # contains 0, 2, 4, 6, 8, 10\n\n    Also any iterable of integers can be specified as first argument:\n\n       >>> RangeSet([3, 6, 8, 7, 1])\n       1,3,6-8\n       >>> rset2 = RangeSet(rset)\n\n    Padding of ranges (eg. "003-009") can be managed through a public RangeSet\n    instance variable named padding. It may be changed at any time. Padding is\n    a simple display feature per RangeSet object, thus current padding value is\n    not taken into account when computing set operations.\n    RangeSet is itself an iterator over its items as integers (instead of\n    strings). To iterate over string items with optional padding, you can use\n    the :meth:`RangeSet.striter`: method.\n\n    RangeSet provides methods like :meth:`RangeSet.union`,\n    :meth:`RangeSet.intersection`, :meth:`RangeSet.difference`,\n    :meth:`RangeSet.symmetric_difference` and their in-place versions\n    :meth:`RangeSet.update`, :meth:`RangeSet.intersection_update`,\n    :meth:`RangeSet.difference_update`,\n    :meth:`RangeSet.symmetric_difference_update` which conform to the Python\n    Set API.\n    '
    _VERSION = 3

    def __init__(self, pattern=None, autostep=None):
        """Initialize RangeSet object.

        :param pattern: optional string pattern
        :param autostep: optional autostep threshold
        """
        if pattern is None or isinstance(pattern, str):
            set.__init__(self)
        else:
            set.__init__(self, pattern)
        if isinstance(pattern, RangeSet):
            self._autostep = pattern._autostep
            self.padding = pattern.padding
        else:
            self._autostep = None
            self.padding = None
        self.autostep = autostep
        if isinstance(pattern, str):
            self._parse(pattern)

    def _parse(self, pattern):
        """Parse string of comma-separated x-y/step -like ranges"""
        for subrange in pattern.split(','):
            if subrange.find('/') < 0:
                baserange, step = subrange, 1
            else:
                baserange, step = subrange.split('/', 1)
            try:
                step = int(step)
            except ValueError:
                raise RangeSetParseError(subrange, 'cannot convert string to integer')

            if baserange.find('-') < 0:
                if step != 1:
                    raise RangeSetParseError(subrange, 'invalid step usage')
                begin = end = baserange
            else:
                begin, end = baserange.split('-', 1)
            try:
                pad = 0
                if int(begin) != 0:
                    begins = begin.lstrip('0')
                    if len(begin) - len(begins) > 0:
                        pad = len(begin)
                    start = int(begins)
                else:
                    if len(begin) > 1:
                        pad = len(begin)
                    start = 0
                if int(end) != 0:
                    ends = end.lstrip('0')
                else:
                    ends = end
                stop = int(ends)
            except ValueError:
                if len(subrange) == 0:
                    msg = 'empty range'
                else:
                    msg = 'cannot convert string to integer'
                raise RangeSetParseError(subrange, msg)

            if stop > 1e+100 or start > stop or step < 1:
                raise RangeSetParseError(subrange, 'invalid values in range')
            self.add_range(start, stop + 1, step, pad)

    @classmethod
    def fromlist(cls, rnglist, autostep=None):
        """Class method that returns a new RangeSet with ranges from provided
        list."""
        inst = RangeSet(autostep=autostep)
        inst.updaten(rnglist)
        return inst

    @classmethod
    def fromone(cls, index, pad=0, autostep=None):
        """Class method that returns a new RangeSet of one single item or
        a single range (from integer or slice object)."""
        inst = RangeSet(autostep=autostep)
        try:
            inst.add(index, pad)
        except TypeError:
            if not index.stop:
                raise ValueError('Invalid range upper limit (%s)' % index.stop)
            inst.add_range(index.start or 0, index.stop, index.step or 1, pad)

        return inst

    def get_autostep(self):
        """Get autostep value (property)"""
        if self._autostep >= AUTOSTEP_DISABLED:
            return
        else:
            return self._autostep + 1

    def set_autostep(self, val):
        """Set autostep value (property)"""
        if val is None:
            self._autostep = AUTOSTEP_DISABLED
        else:
            self._autostep = int(val) - 1

    autostep = property(get_autostep, set_autostep)

    def dim(self):
        """Get the number of dimensions of this RangeSet object. Common
        method with RangeSetND.  Here, it will always return 1 unless
        the object is empty, in that case it will return 0."""
        return int(len(self) > 0)

    def _sorted(self):
        """Get sorted list from inner set."""
        return sorted(set.__iter__(self))

    def __iter__(self):
        """Iterate over each element in RangeSet."""
        return iter(self._sorted())

    def striter(self):
        """Iterate over each (optionally padded) string element in RangeSet."""
        pad = self.padding or 0
        for i in self._sorted():
            yield '%0*d' % (pad, i)

    def contiguous(self):
        """Object-based iterator over contiguous range sets."""
        pad = self.padding or 0
        for sli in self._contiguous_slices():
            yield RangeSet.fromone(slice(sli.start, sli.stop, sli.step), pad)

    def __reduce__(self):
        """Return state information for pickling."""
        return (
         self.__class__, (str(self),),
         {'padding':self.padding, 
          '_autostep':self._autostep, 
          '_version':RangeSet._VERSION})

    def __setstate__(self, dic):
        """called upon unpickling"""
        self.__dict__.update(dic)
        if getattr(self, '_version', 0) < RangeSet._VERSION:
            if getattr(self, '_version', 0) <= 1:
                setattr(self, '_ranges', [(slice(start, stop + 1, step), pad) for start, stop, step, pad in getattr(self, '_ranges')])
            else:
                if hasattr(self, '_ranges'):
                    self_ranges = getattr(self, '_ranges')
                    if self_ranges:
                        if not isinstance(self_ranges[0][0], slice):
                            setattr(self, '_ranges', [(slice(start, stop, step), pad) for (start, stop, step), pad in self_ranges])
            for sli, pad in getattr(self, '_ranges'):
                self.add_range(sli.start, sli.stop, sli.step, pad)

            delattr(self, '_ranges')
            delattr(self, '_length')
        if not hasattr(self, 'padding'):
            setattr(self, 'padding', None)

    def _strslices(self):
        """Stringify slices list (x-y/step format)"""
        pad = self.padding or 0
        for sli in self.slices():
            if sli.start + 1 == sli.stop:
                yield '%0*d' % (pad, sli.start)
            else:
                assert sli.step >= 0, 'Internal error: sli.step < 0'
                if sli.step == 1:
                    yield '%0*d-%0*d' % (pad, sli.start, pad, sli.stop - 1)
                else:
                    yield '%0*d-%0*d/%d' % (pad, sli.start, pad, sli.stop - 1,
                     sli.step)

    def __str__(self):
        """Get comma-separated range-based string (x-y/step format)."""
        return ','.join(self._strslices())

    __repr__ = __str__

    def _contiguous_slices(self):
        """Internal iterator over contiguous slices in RangeSet."""
        k = j = None
        for i in self._sorted():
            if k is None:
                k = j = i
            if i - j > 1:
                yield slice(k, j + 1, 1)
                k = i
            j = i

        if k is not None:
            yield slice(k, j + 1, 1)

    def _folded_slices(self):
        """Internal generator that is able to retrieve ranges organized by
        step."""
        if len(self) == 0:
            return
        else:
            prng = None
            istart = None
            step = 0
            for sli in self._contiguous_slices():
                start = sli.start
                stop = sli.stop
                unitary = start + 1 == stop
                if istart is None:
                    if unitary:
                        istart = start
                    else:
                        prng = [
                         start, stop, 1]
                        istart = stop - 1
                    i = k = istart
                else:
                    if step == 0:
                        if not unitary:
                            if prng is not None:
                                yield slice(*prng)
                            else:
                                yield slice(istart, istart + 1, 1)
                            prng = [
                             start, stop, 1]
                            istart = k = stop - 1
                            continue
                        i = start
                    elif not step > 0:
                        raise AssertionError
                i = start
                if step != i - k or not unitary:
                    if step == i - k:
                        j = i
                    else:
                        j = k
                    stepped = j - istart >= self._autostep * step
                    if prng:
                        if stepped:
                            prng[1] -= 1
                        else:
                            istart += step
                        yield slice(*prng)
                        prng = None
                if step != i - k:
                    if stepped:
                        yield slice(istart, k + 1, step)
                    else:
                        for j in range(istart, k - step + 1, step):
                            yield slice(j, j + 1, 1)

                    if not unitary:
                        yield slice(k, k + 1, 1)
                    if unitary:
                        if stepped:
                            istart = i = k = start
                        else:
                            istart = k
                    else:
                        prng = [
                         start, stop, 1]
                        istart = i = k = stop - 1
                else:
                    if not unitary:
                        if stepped:
                            yield slice(istart, i + 1, step)
                            i += 1
                        else:
                            for j in range(istart, i - step + 1, step):
                                yield slice(j, j + 1, 1)

                        if stop > i + 1:
                            prng = [
                             i, stop, 1]
                        istart = i = k = stop - 1
                    step = i - k
                    k = i

            if step == 0:
                if prng:
                    yield slice(*prng)
                else:
                    yield slice(istart, istart + 1, 1)
            elif not step > 0:
                raise AssertionError
            else:
                stepped = k - istart >= self._autostep * step
                if prng:
                    if stepped:
                        prng[1] -= 1
                    else:
                        istart += step
                    yield slice(*prng)
                    prng = None
                if stepped:
                    yield slice(istart, i + 1, step)
                else:
                    for j in range(istart, i + 1, step):
                        yield slice(j, j + 1, 1)

    def slices(self):
        """
        Iterate over RangeSet ranges as Python slice objects.
        """
        if self._autostep >= AUTOSTEP_DISABLED:
            return self._contiguous_slices()
        else:
            return self._folded_slices()

    def __getitem__(self, index):
        """
        Return the element at index or a subrange when a slice is specified.
        """
        if isinstance(index, slice):
            inst = RangeSet()
            inst._autostep = self._autostep
            inst.padding = self.padding
            inst.update(self._sorted()[index])
            return inst
        if isinstance(index, int):
            return self._sorted()[index]
        raise TypeError('%s indices must be integers' % self.__class__.__name__)

    def split(self, nbr):
        """
        Split the rangeset into nbr sub-rangesets (at most). Each
        sub-rangeset will have the same number of elements more or
        less 1. Current rangeset remains unmodified. Returns an
        iterator.

        >>> RangeSet("1-5").split(3) 
        RangeSet("1-2")
        RangeSet("3-4")
        RangeSet("foo5")
        """
        assert nbr > 0
        slice_size = len(self) // int(nbr)
        left = len(self) % nbr
        begin = 0
        for i in range(0, min(nbr, len(self))):
            length = slice_size + int(i < left)
            yield self[begin:begin + length]
            begin += length

    def add_range(self, start, stop, step=1, pad=0):
        """
        Add a range (start, stop, step and padding length) to RangeSet.
        Like the Python built-in function *range()*, the last element
        is the largest start + i * step less than stop.
        """
        if not start < stop:
            raise AssertionError('please provide ordered node index ranges')
        elif not step > 0:
            raise AssertionError
        elif not pad >= 0:
            raise AssertionError
        else:
            assert stop - start < 1000000000.0, 'range too large'
            if pad is not None:
                if pad > 0:
                    if self.padding is None:
                        self.padding = pad
        set.update(self, range(start, stop, step))

    def copy(self):
        """Return a shallow copy of a RangeSet."""
        cpy = self.__class__()
        cpy._autostep = self._autostep
        cpy.padding = self.padding
        cpy.update(self)
        return cpy

    __copy__ = copy

    def __eq__(self, other):
        """
        RangeSet equality comparison.
        """
        if not isinstance(other, RangeSet):
            return NotImplemented
        else:
            return len(self) == len(other) and self.issubset(other)

    def __or__(self, other):
        """Return the union of two RangeSets as a new RangeSet.

        (I.e. all elements that are in either set.)
        """
        if not isinstance(other, set):
            return NotImplemented
        else:
            return self.union(other)

    def union(self, other):
        """Return the union of two RangeSets as a new RangeSet.

        (I.e. all elements that are in either set.)
        """
        self_copy = self.copy()
        self_copy.update(other)
        return self_copy

    def __and__(self, other):
        """Return the intersection of two RangeSets as a new RangeSet.

        (I.e. all elements that are in both sets.)
        """
        if not isinstance(other, set):
            return NotImplemented
        else:
            return self.intersection(other)

    def intersection(self, other):
        """Return the intersection of two RangeSets as a new RangeSet.

        (I.e. all elements that are in both sets.)
        """
        self_copy = self.copy()
        self_copy.intersection_update(other)
        return self_copy

    def __xor__(self, other):
        """Return the symmetric difference of two RangeSets as a new RangeSet.

        (I.e. all elements that are in exactly one of the sets.)
        """
        if not isinstance(other, set):
            return NotImplemented
        else:
            return self.symmetric_difference(other)

    def symmetric_difference(self, other):
        """Return the symmetric difference of two RangeSets as a new RangeSet.

        (ie. all elements that are in exactly one of the sets.)
        """
        self_copy = self.copy()
        self_copy.symmetric_difference_update(other)
        return self_copy

    def __sub__(self, other):
        """Return the difference of two RangeSets as a new RangeSet.

        (I.e. all elements that are in this set and not in the other.)
        """
        if not isinstance(other, set):
            return NotImplemented
        else:
            return self.difference(other)

    def difference(self, other):
        """Return the difference of two RangeSets as a new RangeSet.

        (I.e. all elements that are in this set and not in the other.)
        """
        self_copy = self.copy()
        self_copy.difference_update(other)
        return self_copy

    def __contains__(self, element):
        """Report whether an element is a member of a RangeSet.
        Element can be either another RangeSet object, a string or an
        integer.

        Called in response to the expression ``element in self``.
        """
        if isinstance(element, set):
            return element.issubset(self)
        else:
            return set.__contains__(self, int(element))

    def issubset(self, other):
        """Report whether another set contains this RangeSet."""
        self._binary_sanity_check(other)
        return set.issubset(self, other)

    def issuperset(self, other):
        """Report whether this RangeSet contains another set."""
        self._binary_sanity_check(other)
        return set.issuperset(self, other)

    __le__ = issubset
    __ge__ = issuperset

    def __lt__(self, other):
        self._binary_sanity_check(other)
        return len(self) < len(other) and self.issubset(other)

    def __gt__(self, other):
        self._binary_sanity_check(other)
        return len(self) > len(other) and self.issuperset(other)

    def _binary_sanity_check(self, other):
        """Check that the other argument to a binary operation is also  a set,
        raising a TypeError otherwise."""
        if not isinstance(other, set):
            raise TypeError('Binary operation only permitted between sets')

    def __ior__(self, other):
        """Update a RangeSet with the union of itself and another."""
        self._binary_sanity_check(other)
        set.__ior__(self, other)
        return self

    def union_update(self, other):
        """Update a RangeSet with the union of itself and another."""
        self.update(other)

    def __iand__(self, other):
        """Update a RangeSet with the intersection of itself and another."""
        self._binary_sanity_check(other)
        set.__iand__(self, other)
        return self

    def intersection_update(self, other):
        """Update a RangeSet with the intersection of itself and another."""
        set.intersection_update(self, other)

    def __ixor__(self, other):
        """Update a RangeSet with the symmetric difference of itself and
        another."""
        self._binary_sanity_check(other)
        set.symmetric_difference_update(self, other)
        return self

    def symmetric_difference_update(self, other):
        """Update a RangeSet with the symmetric difference of itself and
        another."""
        set.symmetric_difference_update(self, other)

    def __isub__(self, other):
        """Remove all elements of another set from this RangeSet."""
        self._binary_sanity_check(other)
        set.difference_update(self, other)
        return self

    def difference_update(self, other, strict=False):
        """Remove all elements of another set from this RangeSet.

        If strict is True, raise KeyError if an element cannot be removed.
        (strict is a RangeSet addition)"""
        if strict:
            if other not in self:
                raise KeyError(set.difference(other, self).pop())
        set.difference_update(self, other)

    def update(self, iterable):
        """Add all integers from an iterable (such as a list)."""
        if isinstance(iterable, RangeSet):
            if self.padding is None:
                if iterable.padding is not None:
                    self.padding = iterable.padding
        elif not not isinstance(iterable, str):
            raise AssertionError
        set.update(self, iterable)

    def updaten(self, rangesets):
        """
        Update a rangeset with the union of itself and several others.
        """
        for rng in rangesets:
            if isinstance(rng, set):
                self.update(rng)
            else:
                self.update(RangeSet(rng))

    def clear(self):
        """Remove all elements from this RangeSet."""
        set.clear(self)
        self.padding = None

    def add(self, element, pad=0):
        """Add an element to a RangeSet.
        This has no effect if the element is already present.
        """
        if pad is not None:
            if pad > 0:
                if self.padding is None:
                    self.padding = pad
        set.add(self, int(element))

    def remove(self, element):
        """Remove an element from a RangeSet; it must be a member.

        :param element: the element to remove
        :raises KeyError: element is not contained in RangeSet
        :raises ValueError: element is not castable to integer
        """
        set.remove(self, int(element))

    def discard(self, element):
        """Remove element from the RangeSet if it is a member.

        If the element is not a member, do nothing.
        """
        try:
            i = int(element)
            set.discard(self, i)
        except ValueError:
            pass


class RangeSetND(object):
    __doc__ = '\n    Build a N-dimensional RangeSet object.\n\n    .. warning:: You don\'t usually need to use this class directly, use\n        :class:`.NodeSet` instead that has ND support.\n\n    Empty constructor::\n\n        RangeSetND()\n\n    Build from a list of list of :class:`RangeSet` objects::\n\n        RangeSetND([[rs1, rs2, rs3, ...], ...])\n\n    Strings are also supported::\n\n        RangeSetND([["0-3", "4-10", ...], ...])\n\n    Integers are also supported::\n\n        RangeSetND([(0, 4), (0, 5), (1, 4), (1, 5), ...]\n    '

    def __init__(self, args=None, pads=None, autostep=None, copy_rangeset=True):
        """RangeSetND initializer

        All parameters are optional.

        :param args: generic "list of list" input argument (default is None)
        :param pads: list of 0-padding length (default is to not pad any
                     dimensions)
        :param autostep: autostep threshold (use range/step notation if more
                         than #autostep items meet the condition) - default is
                         off (None)
        :param copy_rangeset: (advanced) if set to False, do not copy RangeSet
                              objects from args (transfer ownership), which is
                              faster. In that case, you should not modify these
                              objects afterwards (default is True).
        """
        self._veclist = []
        self._dirty = True
        self._autostep = None
        self.autostep = autostep
        self._multivar_hint = False
        if args is None:
            return
        for rgvec in args:
            if rgvec:
                if isinstance(rgvec[0], str):
                    self._veclist.append([RangeSet(rg, autostep=autostep) for rg in rgvec])
                else:
                    if isinstance(rgvec[0], RangeSet):
                        if copy_rangeset:
                            self._veclist.append([rg.copy() for rg in rgvec])
                        else:
                            self._veclist.append(rgvec)
                    else:
                        if pads is None:
                            self._veclist.append([RangeSet.fromone(rg, autostep=autostep) for rg in rgvec])
                        else:
                            self._veclist.append([RangeSet.fromone(rg, pad, autostep) for rg, pad in zip(rgvec, pads)])

    class precond_fold(object):
        __doc__ = 'Decorator to ease internal folding management'

        def __call__(self, func):

            def inner(*args, **kwargs):
                rgnd, fargs = args[0], args[1:]
                if rgnd._dirty:
                    rgnd._fold()
                return func(rgnd, *fargs, **kwargs)

            inner.__name__ = func.__name__
            inner.__doc__ = func.__doc__
            inner.__dict__ = func.__dict__
            inner.__module__ = func.__module__
            return inner

    @precond_fold()
    def copy(self):
        """Return a new, mutable shallow copy of a RangeSetND."""
        cpy = self.__class__()
        cpy._veclist = [[rg.copy() for rg in rgvec] for rgvec in self._veclist]
        cpy._dirty = self._dirty
        return cpy

    __copy__ = copy

    def __eq__(self, other):
        """RangeSetND equality comparison."""
        if not isinstance(other, RangeSetND):
            return NotImplemented
        else:
            return len(self) == len(other) and self.issubset(other)

    def __bool__(self):
        return bool(self._veclist)

    __nonzero__ = __bool__

    def __len__(self):
        """Count unique elements in N-dimensional rangeset."""
        return sum([reduce(mul, [len(rg) for rg in rgvec]) for rgvec in self.veclist])

    @precond_fold()
    def __str__(self):
        """String representation of N-dimensional RangeSet."""
        result = ''
        for rgvec in self._veclist:
            result += '; '.join([str(rg) for rg in rgvec])
            result += '\n'

        return result

    @precond_fold()
    def __iter__(self):
        return self._iter()

    def _iter(self):
        """Iterate through individual items as tuples."""
        for vec in self._veclist:
            for ivec in product(*vec):
                yield ivec

    @precond_fold()
    def iter_padding(self):
        """Iterate through individual items as tuples with padding info."""
        for vec in self._veclist:
            for ivec in product(*vec):
                yield (
                 ivec, [rg.padding for rg in vec])

    @precond_fold()
    def _get_veclist(self):
        """Get folded veclist"""
        return self._veclist

    def _set_veclist(self, val):
        """Set veclist and set dirty flag for deferred folding."""
        self._veclist = val
        self._dirty = True

    veclist = property(_get_veclist, _set_veclist)

    def vectors(self):
        """Get underlying :class:`RangeSet` vectors"""
        return iter(self.veclist)

    def dim(self):
        """Get the current number of dimensions of this RangeSetND
        object.  Return 0 when object is empty."""
        try:
            return len(self._veclist[0])
        except IndexError:
            return 0

    def pads(self):
        """Get a tuple of padding length info for each dimension."""
        pad_veclist = ((rg.padding or 0 for rg in vec) for vec in self._veclist)
        return tuple(max(pads) for pads in zip(*pad_veclist))

    def get_autostep(self):
        """Get autostep value (property)"""
        if self._autostep >= AUTOSTEP_DISABLED:
            return
        else:
            return self._autostep + 1

    def set_autostep(self, val):
        """Set autostep value (property)"""
        if val is None:
            self._autostep = AUTOSTEP_DISABLED
        else:
            self._autostep = int(val) - 1
        for rgvec in self._veclist:
            for rg in rgvec:
                rg._autostep = self._autostep

    autostep = property(get_autostep, set_autostep)

    @precond_fold()
    def __getitem__(self, index):
        """
        Return the element at index or a subrange when a slice is specified.
        """
        if isinstance(index, slice):
            iveclist = []
            for rgvec in self._veclist:
                iveclist += product(*rgvec)

            assert len(iveclist) == len(self)
            rnd = RangeSetND((iveclist[index]), pads=[rg.padding for rg in self._veclist[0]],
              autostep=(self.autostep))
            return rnd
        else:
            if isinstance(index, int):
                if index < 0:
                    length = len(self)
                    if index >= -length:
                        index = length + index
                    else:
                        raise IndexError('%d out of range' % index)
                length = 0
                for rgvec in self._veclist:
                    cnt = reduce(mul, [len(rg) for rg in rgvec])
                    if length + cnt < index:
                        length += cnt
                    else:
                        for ivec in product(*rgvec):
                            if index == length:
                                return ivec
                            length += 1

                raise IndexError('%d out of range' % index)
            else:
                raise TypeError('%s indices must be integers' % self.__class__.__name__)

    @precond_fold()
    def contiguous(self):
        """Object-based iterator over contiguous range sets."""
        veclist = self._veclist
        try:
            dim = len(veclist[0])
        except IndexError:
            return
        else:
            for dimidx in range(dim):
                new_veclist = []
                for rgvec in veclist:
                    for rgsli in rgvec[dimidx].contiguous():
                        rgvec = list(rgvec)
                        rgvec[dimidx] = rgsli
                        new_veclist.append(rgvec)

                veclist = new_veclist

            for rgvec in veclist:
                yield RangeSetND([rgvec])

    @precond_fold()
    def __contains__(self, element):
        """Report whether an element is a member of a RangeSetND.
        Element can be either another RangeSetND object, a string or
        an integer.

        Called in response to the expression ``element in self``.
        """
        if isinstance(element, RangeSetND):
            rgnd_element = element
        else:
            rgnd_element = RangeSetND([[str(element)]])
        return rgnd_element.issubset(self)

    def issubset(self, other):
        """Report whether another set contains this RangeSetND."""
        self._binary_sanity_check(other)
        return other.issuperset(self)

    @precond_fold()
    def issuperset(self, other):
        """Report whether this RangeSetND contains another RangeSetND."""
        self._binary_sanity_check(other)
        if self.dim() == 1:
            if other.dim() == 1:
                return self._veclist[0][0].issuperset(other._veclist[0][0])
            return other._veclist or True
        else:
            test = other.copy()
            test.difference_update(self)
            return not bool(test)

    __le__ = issubset
    __ge__ = issuperset

    def __lt__(self, other):
        self._binary_sanity_check(other)
        return len(self) < len(other) and self.issubset(other)

    def __gt__(self, other):
        self._binary_sanity_check(other)
        return len(self) > len(other) and self.issuperset(other)

    def _binary_sanity_check(self, other):
        """Check that the other argument to a binary operation is also a
        RangeSetND, raising a TypeError otherwise."""
        if not isinstance(other, RangeSetND):
            msg = 'Binary operation only permitted between RangeSetND'
            raise TypeError(msg)

    def _sort(self):
        """N-dimensional sorting."""

        def rgveckeyfunc(rgvec):
            return (
             -reduce(mul, [len(rg) for rg in rgvec]),
             tuple((-len(rg), rg[0], rg[(-1)]) for rg in rgvec))

        self._veclist.sort(key=rgveckeyfunc)

    @precond_fold()
    def fold(self):
        """Explicit folding call. Please note that folding of RangeSetND
        nD vectors are automatically managed, so you should not have to
        call this method. It may be still useful in some extreme cases
        where the RangeSetND is heavily modified."""
        pass

    def _fold(self):
        """In-place N-dimensional folding."""
        if not self._dirty:
            raise AssertionError
        else:
            if len(self._veclist) > 1:
                self._fold_univariate() or self._fold_multivariate()
            else:
                self._dirty = False

    def _fold_univariate(self):
        """Univariate nD folding. Return True on success and False when
        a multivariate folding is required."""
        dim = self.dim()
        vardim = dimdiff = 0
        if dim > 1:
            for i in range(dim):
                slist = [vec[i] for vec in self._veclist]
                if slist.count(slist[0]) != len(slist):
                    dimdiff += 1
                    if dimdiff > 1:
                        break
                    vardim = i

        univar = dim == 1 or dimdiff == 1
        if univar:
            for vec in self._veclist[1:]:
                self._veclist[0][vardim].update(vec[vardim])

            del self._veclist[1:]
            self._dirty = False
        self._multivar_hint = not univar
        return univar

    def _fold_multivariate(self):
        """Multivariate nD folding"""
        self._fold_multivariate_expand()
        self._sort()
        self._fold_multivariate_merge()
        self._sort()
        self._dirty = False

    def _fold_multivariate_expand(self):
        """Multivariate nD folding: expand [phase 1]"""
        max_length = sum([reduce(mul, [len(rg) for rg in rgvec]) for rgvec in self._veclist])
        if len(self._veclist) * (len(self._veclist) - 1) / 2 > max_length * 10:
            pads = self.pads()
            self._veclist = [[RangeSet.fromone(i, pad=(pads[axis]), autostep=(self.autostep)) for axis, i in enumerate(tvec)] for tvec in set(self._iter())]
            return
        index1, index2 = (0, 1)
        while index1 + 1 < len(self._veclist):
            item1 = self._veclist[index1]
            index2 = index1 + 1
            index1 += 1
            while index2 < len(self._veclist):
                item2 = self._veclist[index2]
                index2 += 1
                new_item = None
                disjoint = False
                suppl = []
                for pos, (rg1, rg2) in enumerate(zip(item1, item2)):
                    if not rg1 & rg2:
                        disjoint = True
                        break
                    if new_item is None:
                        new_item = [
                         None] * len(item1)
                    if rg1 == rg2:
                        new_item[pos] = rg1
                    else:
                        assert rg1 & rg2
                        new_item[pos] = rg1 & rg2
                        if rg1 - rg2:
                            item1_p = item1[0:pos] + [rg1 - rg2] + item1[pos + 1:]
                            suppl.append(item1_p)
                        if rg2 - rg1:
                            item2_p = item2[0:pos] + [rg2 - rg1] + item2[pos + 1:]
                            suppl.append(item2_p)

                if not disjoint:
                    if not new_item is not None:
                        raise AssertionError
                    elif not suppl is not None:
                        raise AssertionError
                    item1 = self._veclist[index1 - 1] = new_item
                    index2 -= 1
                    self._veclist.pop(index2)
                    self._veclist += suppl

    def _fold_multivariate_merge(self):
        """Multivariate nD folding: merge [phase 2]"""
        chg = True
        while chg:
            chg = False
            index1, index2 = (0, 1)
            while index1 + 1 < len(self._veclist):
                item1 = self._veclist[index1]
                index2 = index1 + 1
                index1 += 1
                while index2 < len(self._veclist):
                    item2 = self._veclist[index2]
                    index2 += 1
                    new_item = [None] * len(item1)
                    nb_diff = 0
                    for pos, (rg1, rg2) in enumerate(zip(item1, item2)):
                        if rg1 == rg2:
                            new_item[pos] = rg1
                        elif not rg1 & rg2:
                            nb_diff += 1
                            if nb_diff > 1:
                                break
                            new_item[pos] = rg1 | rg2
                        elif rg1 > rg2 or rg1 < rg2:
                            nb_diff += 1
                            if nb_diff > 1:
                                break
                            new_item[pos] = max(rg1, rg2)
                        else:
                            nb_diff = 2
                            break

                    if nb_diff <= 1:
                        chg = True
                        item1 = self._veclist[index1 - 1] = new_item
                        index2 -= 1
                        self._veclist.pop(index2)

    def __or__(self, other):
        """Return the union of two RangeSetNDs as a new RangeSetND.

        (I.e. all elements that are in either set.)
        """
        if not isinstance(other, RangeSetND):
            return NotImplemented
        else:
            return self.union(other)

    def union(self, other):
        """Return the union of two RangeSetNDs as a new RangeSetND.

        (I.e. all elements that are in either set.)
        """
        rgnd_copy = self.copy()
        rgnd_copy.update(other)
        return rgnd_copy

    def update(self, other):
        """Add all RangeSetND elements to this RangeSetND."""
        if isinstance(other, RangeSetND):
            iterable = other._veclist
        else:
            iterable = other
        for vec in iterable:
            assert isinstance(vec[0], RangeSet)
            cpyvec = []
            for rg in vec:
                cpyrg = rg.copy()
                cpyrg.autostep = self.autostep
                cpyvec.append(cpyrg)

            self._veclist.append(cpyvec)

        self._dirty = True
        if not self._multivar_hint:
            self._fold_univariate()

    union_update = update

    def __ior__(self, other):
        """Update a RangeSetND with the union of itself and another."""
        self._binary_sanity_check(other)
        self.update(other)
        return self

    def __isub__(self, other):
        """Remove all elements of another set from this RangeSetND."""
        self._binary_sanity_check(other)
        self.difference_update(other)
        return self

    def difference_update(self, other, strict=False):
        """Remove all elements of another set from this RangeSetND.

        If strict is True, raise KeyError if an element cannot be removed
        (strict is a RangeSet addition)"""
        if strict:
            if other not in self:
                raise KeyError(other.difference(self)[0])
        ergvx = other._veclist
        rgnd_new = []
        index1 = 0
        while index1 < len(self._veclist):
            rgvec1 = self._veclist[index1]
            procvx1 = [rgvec1]
            nextvx1 = []
            index2 = 0
            while index2 < len(ergvx):
                rgvec2 = ergvx[index2]
                while len(procvx1) > 0:
                    rgproc1 = procvx1.pop(0)
                    tmpvx = []
                    for pos, (rg1, rg2) in enumerate(zip(rgproc1, rgvec2)):
                        if not rg1 == rg2:
                            if rg1 < rg2:
                                pass
                            else:
                                if rg1 & rg2:
                                    tmpvec = list(rgproc1)
                                    tmpvec[pos] = rg1.difference(rg2)
                                    tmpvx.append(tmpvec)
                                else:
                                    tmpvx = [
                                     rgproc1]
                                    break

                    if tmpvx:
                        nextvx1 += tmpvx

                if nextvx1:
                    procvx1 = nextvx1
                    nextvx1 = []
                index2 += 1

            if procvx1:
                rgnd_new += procvx1
            index1 += 1

        self.veclist = rgnd_new

    def __sub__(self, other):
        """Return the difference of two RangeSetNDs as a new RangeSetND.

        (I.e. all elements that are in this set and not in the other.)
        """
        if not isinstance(other, RangeSetND):
            return NotImplemented
        else:
            return self.difference(other)

    def difference(self, other):
        """
        ``s.difference(t)`` returns a new object with elements in s
        but not in t.
        """
        self_copy = self.copy()
        self_copy.difference_update(other)
        return self_copy

    def intersection(self, other):
        """
        ``s.intersection(t)`` returns a new object with elements common
        to s and t.
        """
        self_copy = self.copy()
        self_copy.intersection_update(other)
        return self_copy

    def __and__(self, other):
        """
        Implements the & operator. So ``s & t`` returns a new object
        with elements common to s and t.
        """
        if not isinstance(other, RangeSetND):
            return NotImplemented
        else:
            return self.intersection(other)

    def intersection_update(self, other):
        """
        ``s.intersection_update(t)`` returns nodeset s keeping only
        elements also found in t.
        """
        if other is self:
            return
        tmp_rnd = RangeSetND()
        empty_rset = RangeSet()
        for rgvec in self._veclist:
            for ergvec in other._veclist:
                irgvec = [rg.intersection(erg) for rg, erg in zip(rgvec, ergvec)]
                if empty_rset not in irgvec:
                    tmp_rnd.update([irgvec])

        self.veclist = tmp_rnd.veclist

    def __iand__(self, other):
        """
        Implements the &= operator. So ``s &= t`` returns object s
        keeping only elements also found in t (Python 2.5+ required).
        """
        self._binary_sanity_check(other)
        self.intersection_update(other)
        return self

    def symmetric_difference(self, other):
        """
        ``s.symmetric_difference(t)`` returns the symmetric difference
        of two objects as a new RangeSetND.

        (ie. all items that are in exactly one of the RangeSetND.)
        """
        self_copy = self.copy()
        self_copy.symmetric_difference_update(other)
        return self_copy

    def __xor__(self, other):
        """
        Implement the ^ operator. So ``s ^ t`` returns a new RangeSetND
        with nodes that are in exactly one of the RangeSetND.
        """
        if not isinstance(other, RangeSetND):
            return NotImplemented
        else:
            return self.symmetric_difference(other)

    def symmetric_difference_update(self, other):
        """
        ``s.symmetric_difference_update(t)`` returns RangeSetND s
        keeping all nodes that are in exactly one of the objects.
        """
        diff2 = other.difference(self)
        self.difference_update(other)
        self.update(diff2)

    def __ixor__(self, other):
        """
        Implement the ^= operator. So ``s ^= t`` returns object s after
        keeping all items that are in exactly one of the RangeSetND
        (Python 2.5+ required).
        """
        self._binary_sanity_check(other)
        self.symmetric_difference_update(other)
        return self