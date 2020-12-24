# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/wheel/symengine/compatibility.py
# Compiled at: 2020-03-16 01:41:57
"""
Reimplementations of constructs introduced in later versions of Python than
we support. Also some functions that are needed SymPy-wide and are located
here for easy import.
"""
from __future__ import print_function, division
import operator
from collections import defaultdict
import sys
PY3 = sys.version_info[0] > 2
if PY3:
    class_types = (
     type,)
    integer_types = (int,)
    string_types = (str,)
    long = int
    unicode = str
    unichr = chr

    def u(x):
        return x


    def u_decode(x):
        return x


    Iterator = object
    get_function_code = operator.attrgetter('__code__')
    get_function_globals = operator.attrgetter('__globals__')
    get_function_name = operator.attrgetter('__name__')
    import builtins
    from functools import reduce
    from io import StringIO
    cStringIO = StringIO
    exec_ = getattr(builtins, 'exec')
    xrange = range
else:
    import codecs, types
    class_types = (type, types.ClassType)
    integer_types = (int, long)
    string_types = (str, unicode)
    long = long
    unicode = unicode
    unichr = unichr

    def u(x):
        return codecs.unicode_escape_decode(x)[0]


    def u_decode(x):
        return x.decode('utf-8')


    class Iterator(object):

        def next(self):
            return type(self).__next__(self)


    get_function_code = operator.attrgetter('func_code')
    get_function_globals = operator.attrgetter('func_globals')
    get_function_name = operator.attrgetter('func_name')
    import __builtin__ as builtins
    reduce = reduce
    from StringIO import StringIO
    from cStringIO import StringIO as cStringIO

    def exec_(_code_, _globs_=None, _locs_=None):
        """Execute code in a namespace."""
        if _globs_ is None:
            frame = sys._getframe(1)
            _globs_ = frame.f_globals
            if _locs_ is None:
                _locs_ = frame.f_locals
            del frame
        elif _locs_ is None:
            _locs_ = _globs_
        exec 'exec _code_ in _globs_, _locs_'
        return


    xrange = xrange

def with_metaclass(meta, *bases):
    """
    Create a base class with a metaclass.

    For example, if you have the metaclass

    >>> class Meta(type):
    ...     pass

    Use this as the metaclass by doing

    >>> from symengine.compatibility import with_metaclass
    >>> class MyClass(with_metaclass(Meta, object)):
    ...     pass

    This is equivalent to the Python 2::

        class MyClass(object):
            __metaclass__ = Meta

    or Python 3::

        class MyClass(object, metaclass=Meta):
            pass

    That is, the first argument is the metaclass, and the remaining arguments
    are the base classes. Note that if the base class is just ``object``, you
    may omit it.

    >>> MyClass.__mro__
    (<class 'MyClass'>, <... 'object'>)
    >>> type(MyClass)
    <class 'Meta'>

    """

    class metaclass(meta):
        __call__ = type.__call__
        __init__ = type.__init__

        def __new__(cls, name, this_bases, d):
            if this_bases is None:
                return type.__new__(cls, name, (), d)
            else:
                return meta(name, bases, d)

    return metaclass('NewBase', None, {})


class NotIterable:
    """
    Use this as mixin when creating a class which is not supposed to return
    true when iterable() is called on its instances. I.e. avoid infinite loop
    when calling e.g. list() on the instance
    """
    pass


def iterable(i, exclude=(
 string_types, dict, NotIterable)):
    """
    Return a boolean indicating whether ``i`` is SymPy iterable.
    True also indicates that the iterator is finite, i.e. you e.g.
    call list(...) on the instance.

    When SymPy is working with iterables, it is almost always assuming
    that the iterable is not a string or a mapping, so those are excluded
    by default. If you want a pure Python definition, make exclude=None. To
    exclude multiple items, pass them as a tuple.

    See also: is_sequence

    Examples
    ========

    >>> from sympy.utilities.iterables import iterable
    >>> from sympy import Tuple
    >>> things = [[1], (1,), set([1]), Tuple(1), (j for j in [1, 2]), {1:2}, '1', 1]
    >>> for i in things:
    ...     print('%s %s' % (iterable(i), type(i)))
    True <... 'list'>
    True <... 'tuple'>
    True <... 'set'>
    True <class 'sympy.core.containers.Tuple'>
    True <... 'generator'>
    False <... 'dict'>
    False <... 'str'>
    False <... 'int'>

    >>> iterable({}, exclude=None)
    True
    >>> iterable({}, exclude=str)
    True
    >>> iterable("no", exclude=str)
    False

    """
    try:
        iter(i)
    except TypeError:
        return False

    if exclude:
        return not isinstance(i, exclude)
    return True


def is_sequence(i, include=None):
    """
    Return a boolean indicating whether ``i`` is a sequence in the SymPy
    sense. If anything that fails the test below should be included as
    being a sequence for your application, set 'include' to that object's
    type; multiple types should be passed as a tuple of types.

    Note: although generators can generate a sequence, they often need special
    handling to make sure their elements are captured before the generator is
    exhausted, so these are not included by default in the definition of a
    sequence.

    See also: iterable

    Examples
    ========

    >>> from sympy.utilities.iterables import is_sequence
    >>> from types import GeneratorType
    >>> is_sequence([])
    True
    >>> is_sequence(set())
    False
    >>> is_sequence('abc')
    False
    >>> is_sequence('abc', include=str)
    True
    >>> generator = (c for c in 'abc')
    >>> is_sequence(generator)
    False
    >>> is_sequence(generator, include=(str, GeneratorType))
    True

    """
    return hasattr(i, '__getitem__') and iterable(i) or bool(include) and isinstance(i, include)


try:
    from functools import cmp_to_key
except ImportError:

    def cmp_to_key(mycmp):
        """
        Convert a cmp= function into a key= function
        """

        class K(object):

            def __init__(self, obj, *args):
                self.obj = obj

            def __lt__(self, other):
                return mycmp(self.obj, other.obj) < 0

            def __gt__(self, other):
                return mycmp(self.obj, other.obj) > 0

            def __eq__(self, other):
                return mycmp(self.obj, other.obj) == 0

            def __le__(self, other):
                return mycmp(self.obj, other.obj) <= 0

            def __ge__(self, other):
                return mycmp(self.obj, other.obj) >= 0

            def __ne__(self, other):
                return mycmp(self.obj, other.obj) != 0

        return K


try:
    from itertools import zip_longest
except ImportError:
    from itertools import izip_longest as zip_longest

try:
    from itertools import combinations_with_replacement
except ImportError:

    def combinations_with_replacement(iterable, r):
        """Return r length subsequences of elements from the input iterable
        allowing individual elements to be repeated more than once.

        Combinations are emitted in lexicographic sort order. So, if the
        input iterable is sorted, the combination tuples will be produced
        in sorted order.

        Elements are treated as unique based on their position, not on their
        value. So if the input elements are unique, the generated combinations
        will also be unique.

        See also: combinations

        Examples
        ========

        >>> from sympy.core.compatibility import combinations_with_replacement
        >>> list(combinations_with_replacement('AB', 2))
        [('A', 'A'), ('A', 'B'), ('B', 'B')]
        """
        pool = tuple(iterable)
        n = len(pool)
        if not n and r:
            return
        indices = [
         0] * r
        yield tuple(pool[i] for i in indices)
        while True:
            for i in reversed(range(r)):
                if indices[i] != n - 1:
                    break
            else:
                return

            indices[i:] = [
             indices[i] + 1] * (r - i)
            yield tuple(pool[i] for i in indices)


def as_int(n):
    """
    Convert the argument to a builtin integer.

    The return value is guaranteed to be equal to the input. ValueError is
    raised if the input has a non-integral value.

    Examples
    ========

    >>> from sympy.core.compatibility import as_int
    >>> from sympy import sqrt
    >>> 3.0
    3.0
    >>> as_int(3.0) # convert to int and test for equality
    3
    >>> int(sqrt(10))
    3
    >>> as_int(sqrt(10))
    Traceback (most recent call last):
    ...
    ValueError: ... is not an integer

    """
    try:
        result = int(n)
        if result != n:
            raise TypeError
    except TypeError:
        raise ValueError('%s is not an integer' % n)

    return result


def default_sort_key(item, order=None):
    """Return a key that can be used for sorting.

    The key has the structure:

    (class_key, (len(args), args), exponent.sort_key(), coefficient)

    This key is supplied by the sort_key routine of Basic objects when
    ``item`` is a Basic object or an object (other than a string) that
    sympifies to a Basic object. Otherwise, this function produces the
    key.

    The ``order`` argument is passed along to the sort_key routine and is
    used to determine how the terms *within* an expression are ordered.
    (See examples below) ``order`` options are: 'lex', 'grlex', 'grevlex',
    and reversed values of the same (e.g. 'rev-lex'). The default order
    value is None (which translates to 'lex').

    Examples
    ========

    >>> from sympy import S, I, default_sort_key
    >>> from sympy.core.function import UndefinedFunction
    >>> from sympy.abc import x

    The following are equivalent ways of getting the key for an object:

    >>> x.sort_key() == default_sort_key(x)
    True

    Here are some examples of the key that is produced:

    >>> default_sort_key(UndefinedFunction('f'))
    ((0, 0, 'UndefinedFunction'), (1, ('f',)), ((1, 0, 'Number'),
        (0, ()), (), 1), 1)
    >>> default_sort_key('1')
    ((0, 0, 'str'), (1, ('1',)), ((1, 0, 'Number'), (0, ()), (), 1), 1)
    >>> default_sort_key(S.One)
    ((1, 0, 'Number'), (0, ()), (), 1)
    >>> default_sort_key(2)
    ((1, 0, 'Number'), (0, ()), (), 2)

    While sort_key is a method only defined for SymPy objects,
    default_sort_key will accept anything as an argument so it is
    more robust as a sorting key. For the following, using key=
    lambda i: i.sort_key() would fail because 2 doesn't have a sort_key
    method; that's why default_sort_key is used. Note, that it also
    handles sympification of non-string items likes ints:

    >>> a = [2, I, -I]
    >>> sorted(a, key=default_sort_key)
    [2, -I, I]

    The returned key can be used anywhere that a key can be specified for
    a function, e.g. sort, min, max, etc...:

    >>> a.sort(key=default_sort_key); a[0]
    2
    >>> min(a, key=default_sort_key)
    2

    Note
    ----

    The key returned is useful for getting items into a canonical order
    that will be the same across platforms. It is not directly useful for
    sorting lists of expressions:

    >>> a, b = x, 1/x

    Since ``a`` has only 1 term, its value of sort_key is unaffected by
    ``order``:

    >>> a.sort_key() == a.sort_key('rev-lex')
    True

    If ``a`` and ``b`` are combined then the key will differ because there
    are terms that can be ordered:

    >>> eq = a + b
    >>> eq.sort_key() == eq.sort_key('rev-lex')
    False
    >>> eq.as_ordered_terms()
    [x, 1/x]
    >>> eq.as_ordered_terms('rev-lex')
    [1/x, x]

    But since the keys for each of these terms are independent of ``order``'s
    value, they don't sort differently when they appear separately in a list:

    >>> sorted(eq.args, key=default_sort_key)
    [1/x, x]
    >>> sorted(eq.args, key=lambda i: default_sort_key(i, order='rev-lex'))
    [1/x, x]

    The order of terms obtained when using these keys is the order that would
    be obtained if those terms were *factors* in a product.

    See Also
    ========

    sympy.core.expr.as_ordered_factors, sympy.core.expr.as_ordered_terms

    """
    from sympy.core import S, Basic
    from sympy.core.sympify import sympify, SympifyError
    from sympy.core.compatibility import iterable
    if isinstance(item, Basic):
        return item.sort_key(order=order)
    if iterable(item, exclude=string_types):
        if isinstance(item, dict):
            args = item.items()
            unordered = True
        elif isinstance(item, set):
            args = item
            unordered = True
        else:
            args = list(item)
            unordered = False
        args = [ default_sort_key(arg, order=order) for arg in args ]
        if unordered:
            args = sorted(args)
        cls_index, args = 10, (len(args), tuple(args))
    else:
        if not isinstance(item, string_types):
            try:
                item = sympify(item)
            except SympifyError:
                pass
            else:
                if isinstance(item, Basic):
                    return default_sort_key(item)

        cls_index, args = 0, (1, (str(item),))
    return ((cls_index, 0, item.__class__.__name__),
     args, S.One.sort_key(), S.One)


def _nodes(e):
    """
    A helper for ordered() which returns the node count of ``e`` which
    for Basic objects is the number of Basic nodes in the expression tree
    but for other objects is 1 (unless the object is an iterable or dict
    for which the sum of nodes is returned).
    """
    from .basic import Basic
    if isinstance(e, Basic):
        return e.count(Basic)
    else:
        if iterable(e):
            return 1 + sum(_nodes(ei) for ei in e)
        if isinstance(e, dict):
            return 1 + sum(_nodes(k) + _nodes(v) for k, v in e.items())
        return 1


def ordered(seq, keys=None, default=True, warn=False):
    """Return an iterator of the seq where keys are used to break ties in
    a conservative fashion: if, after applying a key, there are no ties
    then no other keys will be computed.

    Two default keys will be applied if 1) keys are not provided or 2) the
    given keys don't resolve all ties (but only if `default` is True). The
    two keys are `_nodes` (which places smaller expressions before large) and
    `default_sort_key` which (if the `sort_key` for an object is defined
    properly) should resolve any ties.

    If ``warn`` is True then an error will be raised if there were no
    keys remaining to break ties. This can be used if it was expected that
    there should be no ties between items that are not identical.

    Examples
    ========

    >>> from sympy.utilities.iterables import ordered
    >>> from sympy import count_ops
    >>> from sympy.abc import x, y

    The count_ops is not sufficient to break ties in this list and the first
    two items appear in their original order (i.e. the sorting is stable):

    >>> list(ordered([y + 2, x + 2, x**2 + y + 3],
    ...    count_ops, default=False, warn=False))
    ...
    [y + 2, x + 2, x**2 + y + 3]

    The default_sort_key allows the tie to be broken:

    >>> list(ordered([y + 2, x + 2, x**2 + y + 3]))
    ...
    [x + 2, y + 2, x**2 + y + 3]

    Here, sequences are sorted by length, then sum:

    >>> seq, keys = [[[1, 2, 1], [0, 3, 1], [1, 1, 3], [2], [1]], [
    ...    lambda x: len(x),
    ...    lambda x: sum(x)]]
    ...
    >>> list(ordered(seq, keys, default=False, warn=False))
    [[1], [2], [1, 2, 1], [0, 3, 1], [1, 1, 3]]

    If ``warn`` is True, an error will be raised if there were not
    enough keys to break ties:

    >>> list(ordered(seq, keys, default=False, warn=True))
    Traceback (most recent call last):
    ...
    ValueError: not enough keys to break ties

    Notes
    =====

    The decorated sort is one of the fastest ways to sort a sequence for
    which special item comparison is desired: the sequence is decorated,
    sorted on the basis of the decoration (e.g. making all letters lower
    case) and then undecorated. If one wants to break ties for items that
    have the same decorated value, a second key can be used. But if the
    second key is expensive to compute then it is inefficient to decorate
    all items with both keys: only those items having identical first key
    values need to be decorated. This function applies keys successively
    only when needed to break ties. By yielding an iterator, use of the
    tie-breaker is delayed as long as possible.

    This function is best used in cases when use of the first key is
    expected to be a good hashing function; if there are no unique hashes
    from application of a key then that key should not have been used. The
    exception, however, is that even if there are many collisions, if the
    first group is small and one does not need to process all items in the
    list then time will not be wasted sorting what one was not interested
    in. For example, if one were looking for the minimum in a list and
    there were several criteria used to define the sort order, then this
    function would be good at returning that quickly if the first group
    of candidates is small relative to the number of items being processed.

    """
    d = defaultdict(list)
    if keys:
        if not isinstance(keys, (list, tuple)):
            keys = [
             keys]
        keys = list(keys)
        f = keys.pop(0)
        for a in seq:
            d[f(a)].append(a)

    else:
        if not default:
            raise ValueError('if default=False then keys must be provided')
        d[None].extend(seq)
    for k in sorted(d.keys()):
        if len(d[k]) > 1:
            if keys:
                d[k] = ordered(d[k], keys, default, warn)
            elif default:
                d[k] = ordered(d[k], (_nodes, default_sort_key), default=False, warn=warn)
            elif warn:
                from sympy.utilities.iterables import uniq
                u = list(uniq(d[k]))
                if len(u) > 1:
                    raise ValueError('not enough keys to break ties: %s' % u)
        for v in d[k]:
            yield v

        d.pop(k)

    return


import os
try:
    try:
        from subprocess import check_output
    except ImportError:
        from subprocess import CalledProcessError, check_call

        def check_output(*args, **kwargs):
            with open(os.devnull, 'w') as (fh):
                kwargs['stdout'] = fh
                try:
                    return check_call(*args, **kwargs)
                except CalledProcessError as e:
                    e.output = 'program output is not available for Python 2.6.x'
                    raise e


except ImportError:
    pass

from collections import namedtuple
from functools import update_wrapper
from threading import RLock
_CacheInfo = namedtuple('CacheInfo', ['hits', 'misses', 'maxsize', 'currsize'])

class _HashedSeq(list):
    __slots__ = 'hashvalue'

    def __init__(self, tup, hash=hash):
        self[:] = tup
        self.hashvalue = hash(tup)

    def __hash__(self):
        return self.hashvalue


def _make_key(args, kwds, typed, kwd_mark=(
 object(),), fasttypes=set((int, str, frozenset, type(None))), sorted=sorted, tuple=tuple, type=type, len=len):
    """Make a cache key from optionally typed positional and keyword arguments"""
    key = args
    if kwds:
        sorted_items = sorted(kwds.items())
        key += kwd_mark
        for item in sorted_items:
            key += item

    if typed:
        key += tuple(type(v) for v in args)
        if kwds:
            key += tuple(type(v) for k, v in sorted_items)
    elif len(key) == 1 and type(key[0]) in fasttypes:
        return key[0]
    return _HashedSeq(key)


def lru_cache(maxsize=100, typed=False):
    """Least-recently-used cache decorator.

    If *maxsize* is set to None, the LRU features are disabled and the cache
    can grow without bound.

    If *typed* is True, arguments of different types will be cached separately.
    For example, f(3.0) and f(3) will be treated as distinct calls with
    distinct results.

    Arguments to the cached function must be hashable.

    View the cache statistics named tuple (hits, misses, maxsize, currsize) with
    f.cache_info().  Clear the cache and statistics with f.cache_clear().
    Access the underlying function with f.__wrapped__.

    See:  http://en.wikipedia.org/wiki/Cache_algorithms#Least_Recently_Used

    """

    def decorating_function(user_function):
        cache = dict()
        stats = [0, 0]
        HITS, MISSES = (0, 1)
        make_key = _make_key
        cache_get = cache.get
        _len = len
        lock = RLock()
        root = []
        root[:] = [root, root, None, None]
        nonlocal_root = [root]
        PREV, NEXT, KEY, RESULT = (0, 1, 2, 3)
        if maxsize == 0:

            def wrapper(*args, **kwds):
                result = user_function(*args, **kwds)
                stats[MISSES] += 1
                return result

        elif maxsize is None:

            def wrapper(*args, **kwds):
                key = make_key(args, kwds, typed)
                result = cache_get(key, root)
                if result is not root:
                    stats[HITS] += 1
                    return result
                result = user_function(*args, **kwds)
                cache[key] = result
                stats[MISSES] += 1
                return result

        else:

            def wrapper(*args, **kwds):
                try:
                    key = make_key(args, kwds, typed) if kwds or typed else args
                except TypeError:
                    stats[MISSES] += 1
                    return user_function(*args, **kwds)

                with lock:
                    link = cache_get(key)
                    if link is not None:
                        root, = nonlocal_root
                        link_prev, link_next, key, result = link
                        link_prev[NEXT] = link_next
                        link_next[PREV] = link_prev
                        last = root[PREV]
                        last[NEXT] = root[PREV] = link
                        link[PREV] = last
                        link[NEXT] = root
                        stats[HITS] += 1
                        return result
                result = user_function(*args, **kwds)
                with lock:
                    root, = nonlocal_root
                    if key in cache:
                        pass
                    elif _len(cache) >= maxsize:
                        oldroot = root
                        oldroot[KEY] = key
                        oldroot[RESULT] = result
                        root = nonlocal_root[0] = oldroot[NEXT]
                        oldkey = root[KEY]
                        oldvalue = root[RESULT]
                        root[KEY] = root[RESULT] = None
                        del cache[oldkey]
                        cache[key] = oldroot
                    else:
                        last = root[PREV]
                        link = [last, root, key, result]
                        last[NEXT] = root[PREV] = cache[key] = link
                    stats[MISSES] += 1
                return result

        def cache_info():
            """Report cache statistics"""
            with lock:
                return _CacheInfo(stats[HITS], stats[MISSES], maxsize, len(cache))

        def cache_clear():
            """Clear the cache and cache statistics"""
            with lock:
                cache.clear()
                root = nonlocal_root[0]
                root[:] = [root, root, None, None]
                stats[:] = [0, 0]
            return

        wrapper.__wrapped__ = user_function
        wrapper.cache_info = cache_info
        wrapper.cache_clear = cache_clear
        return update_wrapper(wrapper, user_function)

    return decorating_function


if sys.version_info[:2] >= (3, 3):
    from functools import lru_cache