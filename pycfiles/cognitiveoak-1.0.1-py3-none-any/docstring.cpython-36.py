# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: C:/Users/HDi/Google Drive/ProgramCodes/Released/PyPI/cognitivegeo/cognitivegeo/src\segpy\docstring.py
# Compiled at: 2017-02-16 13:30:26
# Size of source mod 2**32: 1889 bytes
__doc__ = 'Property decorator for the `__doc__` attribute.\n\nUseful for when you want a custom docstring for class instances\nwhile still showing a generic docstring for the class itself.\n\nA naive attempt using `@property` generally breaks Sphinx as\n`cls.__doc__` returns the property object itself, and not a string.\n\nSee the documentation for `docstring_property` for an example.\n'

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
    """DocstringProperty"""

    def __init__(self, class_doc, fget):
        self.class_doc = class_doc
        self.fget = fget

    def __get__(self, obj, type=None):
        if obj is None:
            return self.class_doc
        else:
            return self.fget(obj)

    def __set__(self, obj, value):
        raise AttributeError("can't set attribute")

    def __delete__(self, obj):
        raise AttributeError("can't delete attribute")


if __name__ == '__main__':
    import doctest
    doctest.testmod()