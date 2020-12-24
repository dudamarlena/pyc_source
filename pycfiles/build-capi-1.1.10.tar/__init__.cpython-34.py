# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\build\__init__.py
# Compiled at: 2015-08-07 11:05:43
# Size of source mod 2**32: 2533 bytes
__doc__ = '\nA tiny base class for fluent builders.\n'

class Builder:
    """Builder"""

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