# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\build\__init__.py
# Compiled at: 2015-08-07 11:05:43
# Size of source mod 2**32: 2533 bytes
"""
A tiny base class for fluent builders.
"""

class Builder:
    __doc__ = '\n    A base class for builders, supporting the "with" style of chaining methods.\n    "With" methods are dynamically generated based on the names defined\n    in the \'defaults\' attribute (to be overridden by subclasses) according\n    to the template ``with_{name}``.\n\n    To subclass Builder:\n        1. Define a class attribute (a list of tuples) called ``defaults``.\n        2. Override the ``dict`` method if you need to use a custom dict class\n        3. Define a ``build`` method which performs the required steps to\n           build the object and returns an instance of the object.\n    A \'with\' method for each entry in ``defaults`` will be generated for you.\n\n    >>> class MyBuilder(Builder):\n    ...     # declare the defaults for the builder\n    ...     defaults = [\n    ...         ("abc", 123),\n    ...         ("def", 456),\n    ...         ("xyz", 789)\n    ...     ]\n    ...\n    ...     def build(self):\n    ...         # convert self.data into the object you\'re building\n    ...         return self.data\n    ...\n    >>> result = MyBuilder().with_abc(-1).with_def(-2).build()\n    >>> result == {\'xyz\': 789, \'def\': -2, \'abc\': -1}\n    True\n    '

    def __init__(self):
        self.data = self.dict(self.defaults)

    def __getattr__(self, name):
        if not name.startswith('with_'):
            raise AttributeError(name)
        if name[5:] not in self.data:
            raise AttributeError(name)

        def _with(value):
            '\n            Sets the value of ``"{}"`` in ``self.data``.\n\n            :param value: The value to set.\n            '.format(name[5:])
            self.data[name[5:]] = value
            return self

        _with.__name__ = name
        return _with

    def dict(self, pairs):
        """
        Override me if you want to use a custom :class:`dict`
        subclass for ``self.data``.
        """
        return dict(pairs)


def evaluate_callables(data):
    """
    Call any callable values in the input dictionary;
    return a new dictionary containing the evaluated results.
    Useful for lazily evaluating default values in ``build`` methods.

    >>> data = {"spam": "ham", "eggs": (lambda: 123)}
    >>> result = evaluate_callables(data)
    >>> result == {'eggs': 123, 'spam': 'ham'}
    True
    """
    sequence = ((k, v() if callable(v) else v) for k, v in data.items())
    return type(data)(sequence)