# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/alelog01/git/resource_locker/src/resource_locker/core/potential.py
# Compiled at: 2018-02-01 06:38:36
# Size of source mod 2**32: 898 bytes


class Potential:

    def __init__(self, item, key_gen=None, tag_gen=None, tags=None, **more_tags):
        self.item = item
        self._state = None
        self._key = item if key_gen is None else key_gen(item)
        self._tags = dict(key=(self._key))
        if tags:
            self._tags.update(tags)
        self._tags.update(more_tags)
        if tag_gen:
            self._tags.update(tag_gen(item))

    @property
    def key(self):
        return self._key

    @property
    def tags(self):
        return self._tags

    @property
    def is_fulfilled(self):
        return self._state is True

    @property
    def is_rejected(self):
        return self._state is False

    def fulfill(self):
        self._state = True
        return self

    def reject(self):
        self._state = False
        return self

    def reset(self):
        self._state = None
        return self