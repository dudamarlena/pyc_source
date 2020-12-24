# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/runner/runners/2.166.2/work/1/s/build/lib.macosx-10.9-x86_64-3.5/pycraf/utils/multistate.py
# Compiled at: 2020-04-16 04:29:51
# Size of source mod 2**32: 7225 bytes
__all__ = [
 'MultiState']

class _MultiMeta(type):

    def __new__(cls, *args):
        if not isinstance(args[2]['_attributes'], tuple):
            raise RuntimeError('"_attributes" must be a tuple!')
        if 'set' in args[2]['_attributes']:
            raise RuntimeError('Option "set" not in list of allowed attributes!')
        for attr in args[2]['_attributes']:
            if attr not in args[2]:
                raise RuntimeError('Must set default value for option "{}" during subclass creation!'.format(attr))

        return super().__new__(cls, *args)

    def __setattr__(cls, attr, value):
        raise RuntimeError('Setting attributes directy is not allowed. Use "set" method!')

    def __repr__(cls):
        if hasattr(cls, '__repr__'):
            return getattr(cls, '__repr__')()
        else:
            return super().__repr__()

    def __str__(cls):
        if hasattr(cls, '__str__'):
            return getattr(cls, '__str__')()
        else:
            return super().__repr__()


class MultiState(object, metaclass=_MultiMeta):
    __doc__ = '\n    Multi state subclasses are used to manage global items.\n\n    `MultiState` is a so-called Singleton, which means that no instances\n    can be created. This way, it is guaranteed that only one `MultiState`\n    entity exists. Thus it offers the possibilty to handle a "global"\n    state, because from anywhere in the code, one could query the\n    current state and react to it. One usecase would be to\n    temporarily allow downloading of files, otherwise being forbidden.\n\n    The `MultiState` class is not useful on its own, but you have to\n    subclass it::\n\n        >>> from pycraf.utils import MultiState\n        >>> class MyState(MultiState):\n        ...\n        ...     # define list of allowed attributes\n        ...     _attributes = (\'foo\', \'bar\')\n        ...\n        ...     # set default values\n        ...     foo = 1\n        ...     bar = "guido"\n\n    It is mandatory to provide a tuple of allowed attributes and to\n    create these instance attributes and assign default values.\n    During class creation, this will be validated, for convenience.\n\n    After defining the state class, one can do the following::\n\n        >>> MyState.foo\n        1\n        >>> MyState.set(foo=2)\n        <MultiState MyState>\n        >>> MyState.foo\n        2\n\n    The `set` method returns a context manager,::\n\n        >>> with MyState.set(foo="dave", bar=10):\n        ...     print(MyState.foo, MyState.bar)\n        dave 10\n\n        >>> print(MyState.foo, MyState.bar)\n        2 guido\n\n    which makes it possible to temporarily change the state object and\n    go back to the original value, once the `with` scope has ended.\n\n    Note, that one cannot set the attributes directly (to ensure\n    that the validation method is always run)::\n\n        >>> MyState.foo = 0\n        Traceback (most recent call last):\n        ...\n        RuntimeError: Setting attributes directy is not allowed. Use "set" method!\n\n    Subclasses will generally override `validate` to convert from any\n    of the acceptable inputs (such as strings) to the appropriate\n    internal objects::\n\n        class MyState(MultiState):\n\n            # define list of allowed attributes\n            _attributes = (\'foo\', \'bar\')\n\n            # set default values\n            foo = 1\n            bar = "guido"\n\n            @classmethod\n            def validate(cls, **kwargs):\n                assert isinstance(kwargs[\'foo\'], int)\n                # etc.\n                return kwargs\n\n    Notes\n    -----\n    This class was adapted from the `~astropy.utils.state.ScienceState` class.\n    '
    _attributes = tuple()

    def __init__(self):
        raise RuntimeError('This class is a singleton.  Do not instantiate.')

    @classmethod
    def set(cls, *, _do_validate=True, **kwargs):
        """
        Set the current science state value.
        """
        for k in kwargs:
            if k not in cls._attributes:
                raise ValueError('Option "{}" not in list of allowed attributes!'.format(k))

        class _Context(object):

            def __init__(self, parent, attrs):
                self._parent = parent
                self._values = {}
                for k in attrs:
                    self._values[k] = getattr(parent, k)

            def __enter__(self):
                pass

            def __exit__(self, type, value, tb):
                cls.hook(**self._values)
                for k, v in self._values.items():
                    self._parent.__class__.__class__.__setattr__(self._parent, k, v)

            def __repr__(self):
                return '<MultiState {0}>'.format(self._parent.__name__)

        ctx = _Context(cls, cls._attributes)
        if _do_validate:
            kwargs = cls.validate(**kwargs)
        cls.hook(**kwargs)
        for k, v in kwargs.items():
            cls.__class__.__class__.__setattr__(cls, k, v)

        return ctx

    @classmethod
    def validate(cls, **kwargs):
        """
        Validate the keyword arguments and return the (converted) kwargs
        dictionary.

        You should override this method if you want to enable validation
        of your attributes.

        Notes
        -----
        One doesn't need to validate the following things, as it is already
        take care of by the `MultiState` class:

        - Check that each argument is assigned with a default.
        - Check that the kwargs keys are in _attributes tuple.
        """
        return kwargs

    @classmethod
    def hook(cls, **kwargs):
        """
        A hook which is called everytime when attributes are about to change.

        You should override this method if you want to enable pre-processing
        or monitoring of your attributes. For example, one could use this
        to react to attribute changes::

            >>> from pycraf.utils import MultiState

            >>> class MyState(MultiState):
            ...
            ...     _attributes = ('foo', 'bar')
            ...     foo = 1
            ...     bar = "guido"
            ...
            ...     @classmethod
            ...     def hook(cls, **kwargs):
            ...         if 'bar' in kwargs:
            ...             if kwargs['bar'] != cls.bar:
            ...                 print('{} about to change: {} --> {}'.format(
            ...                     'bar', kwargs['bar'], cls.bar
            ...                     ))
            ...                 # do stuff ...

            >>> _ = MyState.set(bar="david")
            bar about to change: david --> guido
            >>> _ = MyState.set(bar="david")
            >>> _ = MyState.set(bar="guido")
            bar about to change: guido --> david

            >>> with MyState.set(bar="david"):
            ...     pass
            bar about to change: david --> guido
            bar about to change: guido --> david
        """
        pass