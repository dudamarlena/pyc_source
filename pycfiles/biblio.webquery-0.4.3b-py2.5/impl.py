# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/biblio/webquery/impl.py
# Compiled at: 2009-05-06 14:40:42
"""
Various (fragile) implementation details and utilities.

Don't reply on these because they may go away.

"""
__docformat__ = 'restructuredtext en'
try:
    from xml.etree import ElementTree
except:
    from elementtree import ElementTree

__all__ = [
 'ElementTree',
 'ReprObj',
 'normalize_isbn',
 'assert_or_raise']

class ReprObj(object):
    """
        A class with an simple and consistent printable version.
        """
    _repr_fields = []

    def __str__(self):
        return self.__unicode__().encode('utf8')

    def __unicode__(self):
        repr_strs = [ "%s: '%s'" % (field, getattr(self, field)) for field in self._repr_fields
                    ]
        return '%s (%s)' % (self.__class__.__name__, ('; ').join(repr_strs))

    def __repr__(self):
        return str(self)


def assert_or_raise(cond, error_cls, error_msg=None):
    """
        If a condition is not met, raise a assertion with this message.
        """
    if not cond:
        if error_msg:
            error = error_cls(error_msg)
        else:
            error = error_cls()
        raise error


def _doctest():
    import doctest
    doctest.testmod()


if __name__ == '__main__':
    _doctest()