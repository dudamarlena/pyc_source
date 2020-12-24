# uncompyle6 version 3.6.7
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/ally/container/impl/priority.py
# Compiled at: 2013-10-02 09:54:40
__doc__ = '\nCreated on Feb 23, 2013\n\n@package: ally base\n@copyright: 2011 Sourcefabric o.p.s.\n@license: http://www.gnu.org/licenses/gpl-3.0.txt\n@author: Gabriel Nistor\n\nProvides support for priorities.\n'

class Priority:
    """
    Provides priorities.
    """

    def __init__(self, after=None, before=None):
        """
        Create a new priority.
 
        @param after: Priority|None
            The created priority will be after the provided priority.
        @param before: Priority|None
            The created priority will be before the provided priority.
        """
        if before:
            assert isinstance(before, Priority), 'Invalid priority %s' % before
            assert after is None, 'Can only have before or after priority'
            self._group = before._group
            self._group.insert(self._group.index(before), self)
        else:
            if after:
                assert isinstance(after, Priority), 'Invalid priority %s' % after
                self._group = after._group
                self._group.insert(self._group.index(after) + 1, self)
            else:
                self._group = [
                 self]
        for k, priority in enumerate(self._group):
            priority._index = k

        return


def sortByPriorities(itemsList, priority=None, reverse=False):
    """
    Sorts the item list based on priorities.
    
    @param itemsList: list[object]
        The list to be sorted in place.
    @param priority: callable(object)|None
        The function that provides the priority for the provided object, if None the item list is expected to be
        of priorities.
    @param reverse: boolean
        The reverse sorting flag, same as list sort.
    """
    assert isinstance(itemsList, list), 'Invalid item list %s' % itemsList
    if not priority is None:
        assert callable(priority), 'Invalid priority callable %s' % priority
    group = None

    def key(obj):
        nonlocal group
        if priority:
            obj = priority(obj)
        assert isinstance(obj, Priority), 'Invalid priority %s' % obj
        if group is None:
            group = obj._group
        assert obj._group is group, 'Invalid priority %s for group %s' % (obj, group)
        return obj._index

    itemsList.sort(key=key, reverse=reverse)
    return