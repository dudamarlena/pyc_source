# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:/Users/HDi/Google Drive/ProgramCodes/Released/PyPI/cognitivegeo\cognitivegeo\src\segpy\docstring.py
# Compiled at: 2017-02-16 13:30:26
# Size of source mod 2**32: 1889 bytes
"""Property decorator for the `__doc__` attribute.

Useful for when you want a custom docstring for class instances
while still showing a generic docstring for the class itself.

A naive attempt using `@property` generally breaks Sphinx as
`cls.__doc__` returns the property object itself, and not a string.

See the documentation for `docstring_property` for an example.
"""

def docstring_property(class_doc):
    """Property attribute for docstrings.

    Usage
    -----

    >>> class A(object):
    ...     '''Main docstring'''
    ...     def __init__(self, x):
    ...         self.x = x
    ...     @docstring_property(__doc__)
    ...     def __doc__(self):
    ...         return "My value of x is %s." % self.x

    >>> A.__doc__
    'Main docstring'

    >>> a = A(10)
    >>> a.__doc__
    'My value of x is 10.'
    """

    def wrapper(fget):
        return DocstringProperty(class_doc, fget)

    return wrapper


class DocstringProperty(object):
    __doc__ = 'Property for the `__doc__` attribute.\n\n    Different than `property` in the following two ways:\n\n    * When the attribute is accessed from the main class, it returns the value\n      of `class_doc`, *not* the property itself. This is necessary so Sphinx\n      and other documentation tools can access the class docstring.\n\n    * Only supports getting the attribute; setting and deleting raise an\n      `AttributeError`.\n    '

    def __init__(self, class_doc, fget):
        self.class_doc = class_doc
        self.fget = fget

    def __get__(self, obj, type=None):
        if obj is None:
            return self.class_doc
        return self.fget(obj)

    def __set__(self, obj, value):
        raise AttributeError("can't set attribute")

    def __delete__(self, obj):
        raise AttributeError("can't delete attribute")


if __name__ == '__main__':
    import doctest
    doctest.testmod()