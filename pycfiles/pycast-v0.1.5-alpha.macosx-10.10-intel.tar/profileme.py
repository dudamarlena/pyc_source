# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Python/2.7/site-packages/pycast/common/profileme.py
# Compiled at: 2015-05-28 05:27:48
try:
    import cProfile as profile
except ImportError:
    import profile

class _ProfileDecorator(object):
    """Decorator class that build a wrapper around any function.

    :warning: The decorator does not take recursive calls into account!
    """

    def __init__(self, filelocation):
        """Initializes the ProfileMe decorator.

        :param function func:    Function that will be profiles.
        :param string filelocation:    Location for the profiling results.
        """
        super(_ProfileDecorator, self).__init__()
        self._filelocation = filelocation

    def __call__(self, func):
        """Returns a wrapped version of the called function.

        :param function func:    Function that should be wrapped.

        :return:    Returns a wrapped version of the called function.
        :rtype:     function
        """

        def wrapped_func(*args, **kwargs):
            """This function gets executed, if the wrapped function gets called.

            It automatically created a performance profile for the corresponding function call.
            """
            profiler = profile.Profile()
            result = profiler.runcall(func, *args, **kwargs)
            filename = '%s' % self._filelocation
            profiler.dump_stats(filename)
            return result

        self._func = func
        setattr(wrapped_func, '__name__', self._func.__name__)
        setattr(wrapped_func, '__repr__', self._func.__repr__)
        setattr(wrapped_func, '__str__', self._func.__str__)
        setattr(wrapped_func, '__doc__', self._func.__doc__)
        return wrapped_func


profileMe = _ProfileDecorator