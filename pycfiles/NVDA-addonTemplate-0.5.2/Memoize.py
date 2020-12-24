# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\derek_2\Google Drive\nvda-addon-exploded\notepad++\scons-local-2.5.0\SCons\Memoize.py
# Compiled at: 2016-07-07 03:21:32
__revision__ = 'src/engine/SCons/Memoize.py rel_2.5.0:3543:937e55cd78f7 2016/04/09 11:29:54 bdbaddog'
__doc__ = 'Memoizer\n\nA decorator-based implementation to count hits and misses of the computed\nvalues that various methods cache in memory.\n\nUse of this modules assumes that wrapped methods be coded to cache their\nvalues in a consistent way. In particular, it requires that the class uses a\ndictionary named "_memo" to store the cached values.\n\nHere is an example of wrapping a method that returns a computed value,\nwith no input parameters:\n\n    @SCons.Memoize.CountMethodCall\n    def foo(self):\n\n        try:                                                    # Memoization\n            return self._memo[\'foo\']                            # Memoization\n        except KeyError:                                        # Memoization\n            pass                                                # Memoization\n\n        result = self.compute_foo_value()\n\n        self._memo[\'foo\'] = result                              # Memoization\n\n        return result\n\nHere is an example of wrapping a method that will return different values\nbased on one or more input arguments:\n\n    def _bar_key(self, argument):                               # Memoization\n        return argument                                         # Memoization\n\n    @SCons.Memoize.CountDictCall(_bar_key)\n    def bar(self, argument):\n\n        memo_key = argument                                     # Memoization\n        try:                                                    # Memoization\n            memo_dict = self._memo[\'bar\']                       # Memoization\n        except KeyError:                                        # Memoization\n            memo_dict = {}                                      # Memoization\n            self._memo[\'dict\'] = memo_dict                      # Memoization\n        else:                                                   # Memoization\n            try:                                                # Memoization\n                return memo_dict[memo_key]                      # Memoization\n            except KeyError:                                    # Memoization\n                pass                                            # Memoization\n\n        result = self.compute_bar_value(argument)\n\n        memo_dict[memo_key] = result                            # Memoization\n\n        return result\n\nDeciding what to cache is tricky, because different configurations\ncan have radically different performance tradeoffs, and because the\ntradeoffs involved are often so non-obvious.  Consequently, deciding\nwhether or not to cache a given method will likely be more of an art than\na science, but should still be based on available data from this module.\nHere are some VERY GENERAL guidelines about deciding whether or not to\ncache return values from a method that\'s being called a lot:\n\n    --  The first question to ask is, "Can we change the calling code\n        so this method isn\'t called so often?"  Sometimes this can be\n        done by changing the algorithm.  Sometimes the *caller* should\n        be memoized, not the method you\'re looking at.\n\n    --  The memoized function should be timed with multiple configurations\n        to make sure it doesn\'t inadvertently slow down some other\n        configuration.\n\n    --  When memoizing values based on a dictionary key composed of\n        input arguments, you don\'t need to use all of the arguments\n        if some of them don\'t affect the return values.\n\n'
use_memoizer = None
CounterList = {}

class Counter(object):
    """
    Base class for counting memoization hits and misses.

    We expect that the initialization in a matching decorator will
    fill in the correct class name and method name that represents
    the name of the function being counted.
    """

    def __init__(self, cls_name, method_name):
        """
        """
        self.cls_name = cls_name
        self.method_name = method_name
        self.hit = 0
        self.miss = 0

    def key(self):
        return self.cls_name + '.' + self.method_name

    def display(self):
        fmt = '    %7d hits %7d misses    %s()'
        print fmt % (self.hit, self.miss, self.key())

    def __cmp__(self, other):
        try:
            return cmp(self.key(), other.key())
        except AttributeError:
            return 0


class CountValue(Counter):
    """
    A counter class for simple, atomic memoized values.

    A CountValue object should be instantiated in a decorator for each of
    the class's methods that memoizes its return value by simply storing
    the return value in its _memo dictionary.
    """

    def count(self, *args, **kw):
        """ Counts whether the memoized value has already been
            set (a hit) or not (a miss).
        """
        obj = args[0]
        if self.method_name in obj._memo:
            self.hit = self.hit + 1
        else:
            self.miss = self.miss + 1


class CountDict(Counter):
    """
    A counter class for memoized values stored in a dictionary, with
    keys based on the method's input arguments.

    A CountDict object is instantiated in a decorator for each of the
    class's methods that memoizes its return value in a dictionary,
    indexed by some key that can be computed from one or more of
    its input arguments.
    """

    def __init__(self, cls_name, method_name, keymaker):
        """
        """
        Counter.__init__(self, cls_name, method_name)
        self.keymaker = keymaker

    def count(self, *args, **kw):
        """ Counts whether the computed key value is already present
           in the memoization dictionary (a hit) or not (a miss).
        """
        obj = args[0]
        try:
            memo_dict = obj._memo[self.method_name]
        except KeyError:
            self.miss = self.miss + 1

        key = self.keymaker(*args, **kw)
        if key in memo_dict:
            self.hit = self.hit + 1
        else:
            self.miss = self.miss + 1


def Dump(title=None):
    """ Dump the hit/miss count for all the counters
        collected so far.
    """
    global CounterList
    if title:
        print title
    for counter in sorted(CounterList):
        CounterList[counter].display()


def EnableMemoization():
    global use_memoizer
    use_memoizer = 1


def CountMethodCall(fn):
    """ Decorator for counting memoizer hits/misses while retrieving
        a simple value in a class method. It wraps the given method
        fn and uses a CountValue object to keep track of the
        caching statistics.
        Wrapping gets enabled by calling EnableMemoization().
    """
    if use_memoizer:

        def wrapper(self, *args, **kwargs):
            key = self.__class__.__name__ + '.' + fn.__name__
            if key not in CounterList:
                CounterList[key] = CountValue(self.__class__.__name__, fn.__name__)
            CounterList[key].count(self, *args, **kwargs)
            return fn(self, *args, **kwargs)

        wrapper.__name__ = fn.__name__
        return wrapper
    else:
        return fn


def CountDictCall(keyfunc):
    """ Decorator for counting memoizer hits/misses while accessing
        dictionary values with a key-generating function. Like
        CountMethodCall above, it wraps the given method
        fn and uses a CountDict object to keep track of the
        caching statistics. The dict-key function keyfunc has to
        get passed in the decorator call and gets stored in the
        CountDict instance.
        Wrapping gets enabled by calling EnableMemoization().
    """

    def decorator(fn):
        if use_memoizer:

            def wrapper(self, *args, **kwargs):
                key = self.__class__.__name__ + '.' + fn.__name__
                if key not in CounterList:
                    CounterList[key] = CountDict(self.__class__.__name__, fn.__name__, keyfunc)
                CounterList[key].count(self, *args, **kwargs)
                return fn(self, *args, **kwargs)

            wrapper.__name__ = fn.__name__
            return wrapper
        else:
            return fn

    return decorator