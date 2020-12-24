# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Python/2.7/site-packages/pycast/common/decorators.py
# Compiled at: 2015-05-28 05:28:04


def optimized(fn):
    """Decorator that will call the optimized c++ version
    of a pycast function if available rather than theo
    original pycast function

    :param function fn: original pycast function

    :return: return the wrapped function
    :rtype: function
    """

    def _optimized(self, *args, **kwargs):
        """ This method calls the pycastC function if
        optimization is enabled and the pycastC function
        is available.

        :param: PyCastObject self: reference to the calling object. 
                                    Needs to be passed to the pycastC function,
                                    so that all uts members are available.
        :param: list *args: list of arguments the function is called with.
        :param: dict **kwargs: dictionary of parameter  names and values the function has been called with.

        :return result of the function call either from pycast or pycastC module.
        :rtype: function
        """
        if self.optimizationEnabled:
            class_name = self.__class__.__name__
            module = self.__module__.replace('pycast', 'pycastC')
            try:
                imported = __import__('%s.%s' % (module, class_name), globals(), locals(), [fn.__name__])
                function = getattr(imported, fn.__name__)
                return function(self, *args, **kwargs)
            except ImportError:
                print '[WARNING] Could not enable optimization for %s, %s' % (fn.__name__, self)
                return fn(self, *args, **kwargs)

        else:
            return fn(self, *args, **kwargs)

    setattr(_optimized, '__name__', fn.__name__)
    setattr(_optimized, '__repr__', fn.__repr__)
    setattr(_optimized, '__str__', fn.__str__)
    setattr(_optimized, '__doc__', fn.__doc__)
    return _optimized