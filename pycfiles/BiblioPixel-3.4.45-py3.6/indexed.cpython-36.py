# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bibliopixel/animation/indexed.py
# Compiled at: 2019-08-11 12:22:47
# Size of source mod 2**32: 2273 bytes
from .collection import Collection
from ..util import log

class Indexed(Collection):
    __doc__ = '\n    An ``Indexed`` is a :py:class:`bibliopixel.animation.Collection`\n    which keeps track of the current animation through an index into the list of\n    animations, and gets a callback after that index changes.\n\n    An ``Indexed`` has two properties.\n\n    ``index`` is a mutable property indexing the current animation in the list\n    of animations.\n\n    ``current_animation`` returns the animation at position ``index`` or None\n    if it is out of the bounds of the ``Collection``.\n    '
    _index = -1

    @property
    def index(self):
        """
        :returns int: index of the current animation within the Collection.
        """
        return self._index

    @index.setter
    def index(self, index):
        index = self.animations._index(index)
        self._index, old_index = index, self._index
        self._on_index(old_index)

    def _on_index(self, old_index):
        """
        Override this method to get called right after ``self.index`` is set.

        :param int old_index: the previous index, before it was changed.
        """
        if self.animation:
            log.debug('%s: %s', self.__class__.__name__, self.current_animation.title)
            self.frames = self.animation.generate_frames(False)

    def pre_run(self):
        super().pre_run()
        self.index = 0

    def step(self, amt=1):
        try:
            next(self.frames)
            return True
        except StopIteration:
            pass
        except Exception as e:
            if self.fail_on_exception:
                raise
            log.error('Exception %s in wrapper.step()', e)

    def forward(self, *unused):
        self.index += 1

    def backward(self, *unused):
        self.index -= 1

    @property
    def animation(self):
        """
        :returns: the selected animation based on self.index, or None if
            self.index is out of bounds
        """
        if 0 <= self._index < len(self.animations):
            return self.animations[self._index]

    @property
    def current_animation(self):
        """
        DEPRECATED:
        :returns: self.animation
        """
        return self.animation