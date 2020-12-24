# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\peak\util\roles.py
# Compiled at: 2007-10-26 09:59:33
"""This module is DEPRECATED.  Please use AddOns (peak.util.addons) instead"""
from peak.util import addons
__all__ = [
 'Role', 'ClassRole', 'Registry', 'roledict_for']
roledict_for = addons.addons_for

class Role(addons.AddOn):
    """Attach extra state to (almost) any object"""
    __module__ = __name__
    __slots__ = ()
    role_key = classmethod(addons.AddOn.addon_key.im_func)

    def addon_key(cls, *args):
        return cls.role_key(*args)

    addon_key = classmethod(addon_key)


class ClassRole(addons.ClassAddOn, Role):
    """Attachment/annotation for classes and types"""
    __module__ = __name__
    __slots__ = ()

    def delete_from(cls, ob, *key):
        """Class Roles are not deletable!"""
        raise TypeError('ClassRoles cannot be deleted')

    delete_from = classmethod(delete_from)


class Registry(addons.Registry, Role):
    """ClassRole that's a dictionary with mro-based inheritance"""
    __module__ = __name__
    __slots__ = ()


def additional_tests():
    import doctest
    return doctest.DocFileSuite('README.txt', package='__main__', optionflags=doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE)