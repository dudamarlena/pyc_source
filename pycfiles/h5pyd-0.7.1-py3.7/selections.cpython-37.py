# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/h5pyd/_hl/selections.py
# Compiled at: 2019-12-23 20:17:33
# Size of source mod 2**32: 23393 bytes
"""
    High-level access to HDF5 dataspace selections
"""
from __future__ import absolute_import
import numpy as np
H5S_SEL_POINTS = 0
H5S_SELECT_SET = 1
H5S_SELECT_APPEND = 2
H5S_SELECT_PREPEND = 3
H5S_SELECT_OR = 4
H5S_SELECT_NONE = 5
H5S_SELECT_ALL = 6
H5S_SELECT_HYPERSLABS = 7
H5S_SELECT_NOTB = 8

def select(obj, args):
    """ High-level routine to generate a selection from arbitrary arguments
    to __getitem__.  The arguments should be the following:

    obj
        Datatset object

    args
        Either a single argument or a tuple of arguments.  See below for
        supported classes of argument.

    Argument classes:

    Single Selection instance
        Returns the argument.

    numpy.ndarray
        Must be a boolean mask.  Returns a PointSelection instance.

    RegionReference
        Returns a Selection instance.

    Indices, slices, ellipses only
        Returns a SimpleSelection instance

    Indices, slices, ellipses, lists or boolean index arrays
        Returns a FancySelection instance.
    """
    if not isinstance(args, tuple):
        args = (
         args,)
    else:
        if obj.shape == ():
            sel = ScalarSelection(obj.shape, args)
            return sel
        if len(args) == 1:
            arg = args[0]
            if isinstance(arg, Selection):
                if arg.shape != obj.shape:
                    raise TypeError('Mismatched selection shape')
                return arg
            if isinstance(arg, np.ndarray) or isinstance(arg, list):
                sel = PointSelection(obj.shape)
                sel[arg]
                return sel
    for a in args:
        if isinstance(a, slice) or a is not Ellipsis:
            try:
                int(a)
            except Exception:
                sel = FancySelection(obj.shape)
                sel[args]
                return sel

    sel = SimpleSelection(obj.shape)
    sel[args]
    return sel


class Selection(object):
    __doc__ = '\n        Base class for HDF5 dataspace selections.  Subclasses support the\n        "selection protocol", which means they have at least the following\n        members:\n\n        __init__(shape)   => Create a new selection on "shape"-tuple\n        __getitem__(args) => Perform a selection with the range specified.\n                             What args are allowed depends on the\n                             particular subclass in use.\n\n        id (read-only) =>      h5py.h5s.SpaceID instance\n        shape (read-only) =>   The shape of the dataspace.\n        mshape  (read-only) => The shape of the selection region.\n                               Not guaranteed to fit within "shape", although\n                               the total number of points is less than\n                               product(shape).\n        nselect (read-only) => Number of selected points.  Always equal to\n                               product(mshape).\n\n        broadcast(target_shape) => Return an iterable which yields dataspaces\n                                   for read, based on target_shape.\n\n        The base class represents "unshaped" selections (1-D).\n    '

    def __init__(self, shape, *args, **kwds):
        """ Create a selection.  Shape may be None if spaceid is given. """
        shape = tuple(shape)
        self._shape = shape
        self._select_type = H5S_SELECT_ALL

    @property
    def select_type(self):
        """ SpaceID instance """
        return self._select_type

    @property
    def shape(self):
        """ Shape of whole dataspace """
        return self._shape

    @property
    def nselect(self):
        """ Number of elements currently selected """
        return self.getSelectNpoints()

    @property
    def mshape(self):
        """ Shape of selection (always 1-D for this class) """
        return (
         self.nselect,)

    def getSelectNpoints(self):
        npoints = None
        if self._select_type == H5S_SELECT_NONE:
            npoints = 0
        else:
            if self._select_type == H5S_SELECT_ALL:
                dims = self._shape
                npoints = 1
                for nextent in dims:
                    npoints *= nextent

            else:
                raise IOError('Unsupported select type')
        return npoints

    def broadcast(self, target_shape):
        """ Get an iterable for broadcasting """
        if np.product(target_shape) != self.nselect:
            raise TypeError('Broadcasting is not supported for point-wise selections')
        yield self._id

    def __getitem__(self, args):
        raise NotImplementedError('This class does not support indexing')


class PointSelection(Selection):
    __doc__ = '\n        Represents a point-wise selection.  You can supply sequences of\n        points to the three methods append(), prepend() and set(), or a\n        single boolean array to __getitem__.\n    '

    def __init__(self, shape, *args, **kwds):
        """ Create a Point selection.   """
        (Selection.__init__)(self, shape, *args, **kwds)
        self._points = []

    @property
    def points(self):
        """ selection points """
        return self._points

    def getSelectNpoints(self):
        npoints = None
        if self._select_type == H5S_SELECT_NONE:
            npoints = 0
        else:
            if self._select_type == H5S_SELECT_ALL:
                dims = self._shape
                npoints = 1
                for nextent in dims:
                    npoints *= nextent

            else:
                if self._select_type == H5S_SEL_POINTS:
                    dims = self._shape
                    rank = len(dims)
                    if len(self._points) == rank and type(self._points[0]) not in (list, tuple, np.ndarray):
                        npoints = 1
                    else:
                        npoints = len(self._points)
                else:
                    raise IOError('Unsupported select type')
        return npoints

    def _perform_selection(self, points, op):
        """ Internal method which actually performs the selection """
        points = isinstance(points, np.ndarray) or np.asarray(points, order='C', dtype='u8')
        if len(points.shape) == 1:
            pass
        if self._select_type != H5S_SEL_POINTS:
            op = H5S_SELECT_SET
        else:
            self._select_type = H5S_SEL_POINTS
            if op == H5S_SELECT_SET:
                self._points = points
            else:
                if op == H5S_SELECT_APPEND:
                    self._points.extent(points)
                else:
                    if op == H5S_SELECT_PREPEND:
                        tmp = self._points
                        self._points = points
                        self._points.extend(tmp)
                    else:
                        raise ValueError('Unsupported operation')

    def __getitem__(self, arg):
        """ Perform point-wise selection from a NumPy boolean array """
        if isinstance(arg, list):
            points = arg
        else:
            if not (isinstance(arg, np.ndarray) and arg.dtype.kind == 'b'):
                raise TypeError('PointSelection __getitem__ only works with bool arrays')
            if not arg.shape == self._shape:
                raise TypeError('Boolean indexing array has incompatible shape')
            points = np.transpose(arg.nonzero())
        self.set(points)
        return self

    def append(self, points):
        """ Add the sequence of points to the end of the current selection """
        self._perform_selection(points, H5S_SELECT_APPEND)

    def prepend(self, points):
        """ Add the sequence of points to the beginning of the current selection """
        self._perform_selection(points, H5S_SELECT_PREPEND)

    def set(self, points):
        """ Replace the current selection with the given sequence of points"""
        self._perform_selection(points, H5S_SELECT_SET)


class SimpleSelection(Selection):
    __doc__ = ' A single "rectangular" (regular) selection composed of only slices\n        and integer arguments.  Can participate in broadcasting.\n    '

    @property
    def mshape(self):
        """ Shape of current selection """
        return self._mshape

    @property
    def start(self):
        return self._sel[0]

    @property
    def count(self):
        return self._sel[1]

    @property
    def step(self):
        return self._sel[2]

    def __init__(self, shape, *args, **kwds):
        (Selection.__init__)(self, shape, *args, **kwds)
        rank = len(self._shape)
        self._sel = ((0, ) * rank, self._shape, (1, ) * rank, (False, ) * rank)
        self._mshape = self._shape
        self._select_type = H5S_SELECT_ALL

    def __getitem__(self, args):
        if not isinstance(args, tuple):
            args = (
             args,)
        if self._shape == ():
            if len(args) > 0:
                if args[0] not in (Ellipsis, ()):
                    raise TypeError('Invalid index for scalar dataset (only ..., () allowed)')
            self._select_type = H5S_SELECT_ALL
            return self
        start, count, step, scalar = _handle_simple(self._shape, args)
        self._sel = (start, count, step, scalar)
        self._select_type = H5S_SELECT_HYPERSLABS
        self._mshape = tuple((x for x, y in zip(count, scalar) if not y))
        return self

    def getSelectNpoints(self):
        """Return number of elements in current selection
        """
        npoints = None
        if self._select_type == H5S_SELECT_NONE:
            npoints = 0
        else:
            if self._select_type == H5S_SELECT_ALL:
                dims = self._shape
                npoints = 1
                for nextent in dims:
                    npoints *= nextent

            else:
                if self._select_type == H5S_SELECT_HYPERSLABS:
                    dims = self._shape
                    npoints = 1
                    rank = len(dims)
                    for i in range(rank):
                        npoints *= self.count[i]

                else:
                    raise IOError('Unsupported select type')
        return npoints

    def getQueryParam(self):
        param = ''
        rank = len(self._shape)
        if rank == 0:
            return
        param += '['
        for i in range(rank):
            start = self.start[i]
            stop = start + self.count[i] * self.step[i]
            if stop > self._shape[i]:
                stop = self._shape[i]
            dim_sel = str(start) + ':' + str(stop)
            if self.step[i] != 1:
                dim_sel += ':' + str(self.step[i])
            if i != rank - 1:
                dim_sel += ','
            param += dim_sel

        param += ']'
        return param

    def broadcast(self, target_shape):
        """ Return an iterator over target dataspaces for broadcasting.

        Follows the standard NumPy broadcasting rules against the current
        selection shape (self._mshape).
        """
        if self._shape == ():
            if np.product(target_shape) != 1:
                raise TypeError("Can't broadcast %s to scalar" % target_shape)
        else:
            self._id.select_all()
            yield self._id
            return
            start, count, step, scalar = self._sel
            rank = len(count)
            target = list(target_shape)
            tshape = []
            for idx in range(1, rank + 1):
                if len(target) == 0 or scalar[(-idx)]:
                    tshape.append(1)
                else:
                    t = target.pop()
                    if t == 1 or count[(-idx)] == t:
                        tshape.append(t)
                    else:
                        raise TypeError("Can't broadcast %s -> %s" % (target_shape, count))

            tshape.reverse()
            tshape = tuple(tshape)
            chunks = tuple((x // y for x, y in zip(count, tshape)))
            nchunks = int(np.product(chunks))
            if nchunks == 1:
                yield self._id
            else:
                sid = self._id.copy()
                sid.select_hyperslab((0, ) * rank, tshape, step)
                for idx in range(nchunks):
                    offset = tuple((x * y * z + s for x, y, z, s in zip(np.unravel_index(idx, chunks), tshape, step, start)))
                    sid.offset_simple(offset)
                    yield sid


class FancySelection(Selection):
    __doc__ = '\n        Implements advanced NumPy-style selection operations in addition to\n        the standard slice-and-int behavior.\n\n        Indexing arguments may be ints, slices, lists of indicies, or\n        per-axis (1D) boolean arrays.\n\n        Broadcasting is not supported for these selections.\n    '

    @property
    def mshape(self):
        return self._mshape

    @property
    def hyperslabs(self):
        return self._hyperslabs

    def __init__(self, shape, *args, **kwds):
        (Selection.__init__)(self, shape, *args, **kwds)
        self._mshape = self._shape
        self._hyperslabs = []

    def __getitem__(self, args):
        if not isinstance(args, tuple):
            args = (
             args,)
        else:
            args = _expand_ellipsis(args, len(self._shape))
            sequenceargs = {}
            for idx, arg in enumerate(args):
                if isinstance(arg, slice) or hasattr(arg, 'dtype'):
                    if arg.dtype == np.dtype('bool'):
                        if len(arg.shape) != 1:
                            raise TypeError('Boolean indexing arrays must be 1-D')
                        arg = arg.nonzero()[0]
                    else:
                        try:
                            sequenceargs[idx] = list(arg)
                        except TypeError:
                            pass

                    if sorted(arg) != list(arg):
                        raise TypeError('Indexing elements must be in increasing order')

            if len(sequenceargs) > 1:
                raise TypeError('Only one indexing vector or array is currently allowed for advanced selection')
            if len(sequenceargs) == 0:
                raise TypeError('Advanced selection inappropriate')
            vectorlength = len(list(sequenceargs.values())[0])
            assert all((len(x) == vectorlength for x in sequenceargs.values())), 'All sequence arguments must have the same length %s' % sequenceargs
        argvector = []
        for idx in range(vectorlength):
            entry = list(args)
            for position, seq in sequenceargs.items():
                entry[position] = seq[idx]

            argvector.append(entry)

        self._hyperslabs = []
        count = ()
        for idx, vector in enumerate(argvector):
            start, count, step, scalar = _handle_simple(self._shape, vector)
            self._hyperslabs.append({'start':start,  'count':count,  'step':step})

        mshape = list(count)
        for idx in range(len(mshape)):
            if idx in sequenceargs:
                mshape[idx] = len(sequenceargs[idx])

        self._mshape = tuple((x for x in mshape if x != 0))

    def broadcast(self, target_shape):
        if not target_shape == self._mshape:
            raise TypeError('Broadcasting is not supported for complex selections')
        yield self._id


def _expand_ellipsis(args, rank):
    """ Expand ellipsis objects and fill in missing axes.
    """
    n_el = sum((1 for arg in args if arg is Ellipsis))
    if n_el > 1:
        raise ValueError('Only one ellipsis may be used.')
    else:
        if n_el == 0:
            if len(args) != rank:
                args = args + (Ellipsis,)
    final_args = []
    n_args = len(args)
    for arg in args:
        if arg is Ellipsis:
            final_args.extend((slice(None, None, None),) * (rank - n_args + 1))
        else:
            final_args.append(arg)

    if len(final_args) > rank:
        raise TypeError('Argument sequence too long')
    return final_args


def _handle_simple(shape, args):
    """ Process a "simple" selection tuple, containing only slices and
        integer objects.  Return is a 4-tuple with tuples for start,
        count, step, and a flag which tells if the axis is a "scalar"
        selection (indexed by an integer).

        If "args" is shorter than "shape", the remaining axes are fully
        selected.
    """
    args = _expand_ellipsis(args, len(shape))
    start = []
    count = []
    step = []
    scalar = []
    for arg, length in zip(args, shape):
        if isinstance(arg, slice):
            x, y, z = _translate_slice(arg, length)
            s = False
        else:
            try:
                x, y, z = _translate_int(int(arg), length)
                s = True
            except TypeError:
                raise TypeError('Illegal index "%s" (must be a slice or number)' % arg)

            start.append(x)
            count.append(y)
            step.append(z)
            scalar.append(s)

    return (
     tuple(start), tuple(count), tuple(step), tuple(scalar))


def _translate_int(exp, length):
    """ Given an integer index, return a 3-tuple
        (start, count, step)
        for hyperslab selection
    """
    if exp < 0:
        exp = length + exp
    if not 0 <= exp < length:
        raise ValueError('Index (%s) out of range (0-%s)' % (exp, length - 1))
    return (exp, 1, 1)


def _translate_slice(exp, length):
    """ Given a slice object, return a 3-tuple
        (start, count, step)
        for use with the hyperslab selection routines
    """
    start, stop, step = exp.indices(length)
    if step < 1:
        raise ValueError('Step must be >= 1 (got %d)' % step)
    if stop < start:
        raise ValueError('Reverse-order selections are not allowed')
    count = 1 + (stop - start - 1) // step
    return (
     start, count, step)


def guess_shape(sid):
    """ Given a dataspace, try to deduce the shape of the selection.

    Returns one of:
        * A tuple with the selection shape, same length as the dataspace
        * A 1D selection shape for point-based and multiple-hyperslab selections
        * None, for unselected scalars and for NULL dataspaces
    """
    sel_class = sid.get_simple_extent_type()
    sel_type = sid.get_select_type()
    if sel_class == 'H5S_NULL':
        return
        if sel_class == 'H5S_SCALAR':
            if sel_type == H5S_SELECT_NONE:
                return
            if sel_type == H5S_SELECT_ALL:
                return tuple()
    elif sel_class != 'H5S_SIMPLE':
        raise TypeError('Unrecognized dataspace class %s' % sel_class)
    N = sid.get_select_npoints()
    rank = len(sid.shape)
    if sel_type == H5S_SELECT_NONE:
        return (0, ) * rank
    if sel_type == H5S_SELECT_ALL:
        return sid.shape
    if sel_type == H5S_SEL_POINTS:
        return (
         N,)
    if sel_type != H5S_SELECT_HYPERSLABS:
        raise TypeError('Unrecognized selection method %s' % sel_type)
    if N == 0:
        return (0, ) * rank
    bottomcorner, topcorner = (np.array(x) for x in sid.get_select_bounds())
    boxshape = topcorner - bottomcorner + np.ones((rank,))

    def get_n_axis(sid, axis):
        if boxshape[axis] == 1:
            return 1
        start = bottomcorner.copy()
        start[axis] += 1
        count = boxshape.copy()
        count[axis] -= 1
        masked_sid = sid.copy()
        masked_sid.select_hyperslab((tuple(start)), (tuple(count)), op=H5S_SELECT_NOTB)
        N_leftover = masked_sid.get_select_npoints()
        return N // N_leftover

    shape = tuple((get_n_axis(sid, x) for x in range(rank)))
    if np.product(shape) != N:
        return (
         N,)
    return shape


class ScalarSelection(Selection):
    __doc__ = '\n        Implements slicing for scalar datasets.\n    '

    @property
    def mshape(self):
        return self._mshape

    def __init__(self, shape, *args, **kwds):
        (Selection.__init__)(self, shape, *args, **kwds)
        arg = None
        if len(args) > 0:
            arg = args[0]
        elif arg == ():
            self._mshape = None
            self._select_type = H5S_SELECT_ALL
        else:
            if arg == (Ellipsis,):
                self._mshape = ()
                self._select_type = H5S_SELECT_ALL
            else:
                raise ValueError('Illegal slicing argument for scalar dataspace')