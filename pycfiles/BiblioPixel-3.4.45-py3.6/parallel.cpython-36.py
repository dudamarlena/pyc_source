# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bibliopixel/animation/parallel.py
# Compiled at: 2019-08-11 12:22:47
# Size of source mod 2**32: 954 bytes
from . import collection

class Parallel(collection.Collection):
    __doc__ = '\n    A Parallel is a Collection where all the animations are running at the same\n    time - as opposed to the base Collection where only one animation runs\n    at any time.\n    '

    def __init__(self, *args, overlay=False, detach=True, **kwds):
        """
        If overlay is True, then preclear is set to False for everything
        other than the first animation.
        """
        (super().__init__)(*args, **kwds)
        if detach:
            self.detach(overlay)

    def generate_frames(self):
        self._frames = [[a.generate_frames(), True] for a in self.animations]
        return super().generate_frames()

    def step(self, amt=1):
        for i, (frames, enabled) in enumerate(self._frames):
            if enabled:
                try:
                    next(frames)
                except StopIteration:
                    self._frames[i][1] = False