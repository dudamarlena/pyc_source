# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/borg/supergroup/interfaces.py
# Compiled at: 2008-04-05 06:39:05
from zope.interface import Interface

class ISuperGroups(Interface):
    """The plugin will look up subscription adapters on the current user that
    provide this interface.
    """
    __module__ = __name__

    def __call__():
        """Return an iterable of the group ids for the adapted principal
        """
        pass


class ISuperGroupsEnumeration(Interface):
    """The plugin will look up all registered utilities for this interface
    """
    __module__ = __name__

    def enumerate_groups(id=None, exact_match=False, **kw):
        """Return an iterable of group info that match the given id exactly 
        (if exact_match is given), or partially (if not). Group info is a dict
        with keys id, title.
        """
        pass