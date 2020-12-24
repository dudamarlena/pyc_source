# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bryanbriney/git/abtools/abtools/utils/decorators.py
# Compiled at: 2016-12-30 19:19:17


def lazy_property(func):
    """
    Wraps a property to provide lazy evaluation. Eliminates boilerplate.
    Also provides for setting and deleting the property.

    Use as you would use the @property decorator::

        # OLD:
        class MyClass():
            def __init__():
                self._compute = None

            @property
            def compute(self):
                if self._compute is None:
                    # computationally intense stuff
                    # ...
                    # ...
                    self._compute = result
                return self._compute

            @compute.setter
            def compute(self, value):
                self._compute = value

        # NEW:
        class MyClass():

            def __init__():
                pass

            @lazy_property
            def compute(self):
                # computationally intense stuff
                # ...
                # ...
                return result

    .. note:

        Properties wrapped with ``lazy_property`` are only evaluated once.
        If the instance state changes, lazy properties will not be automatically
        re-evaulated and the update must be explicitly called for::

            c = MyClass(data)
            prop = c.lazy_property

            # If you update some data that affects c.lazy_property
            c.data = new_data

            # c.lazy_property won't change
            prop == c.lazy_property  # TRUE

            # If you want to update c.lazy_property, you can delete it, which will
            # force it to be recomputed (with the new data) the next time you use it
            del c.lazy_property
            new_prop = c.lazy_property
            new_prop == prop  # FALSE
    """
    attr_name = '_lazy_' + func.__name__

    @property
    def _lazy_property(self):
        if not hasattr(self, attr_name):
            setattr(self, attr_name, func(self))
        return getattr(self, attr_name)

    @_lazy_property.deleter
    def _lazy_property(self):
        if hasattr(self, attr_name):
            delattr(self, attr_name)

    @_lazy_property.setter
    def _lazy_property(self, value):
        setattr(self, attr_name, value)

    return _lazy_property


def coroutine(func):
    """
    Initializes a coroutine -- essentially it just takes a
    generator function and calls generator.next() to get
    things going.
    """

    def start(*args, **kwargs):
        cr = func(*args, **kwargs)
        cr.next()
        return cr

    return start