# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bibliopixel/builder/builder.py
# Compiled at: 2019-08-11 12:22:47
# Size of source mod 2**32: 2971 bytes
from .pixels import Pixels
from .runner import Runner
from .saved_description import SavedDescription
from .. import colors
from ..commands import animations
from ..drivers.SimPixel import driver as simpixel_driver
from ..project import project
from ..util import log

class Builder(SavedDescription):
    __doc__ = '\n    A Project Builder to allow people to experiment with projects\n    from the command line or in their own main program.\n\n    '
    COLORS = colors.COLORS

    def __init__(self, project_file='', desc=None, threaded=None, **kwds):
        self.project = None
        self.pixel = Pixels(self)
        self._runner = Runner(self)
        (super().__init__)(project_file, desc, **kwds)
        if threaded is not None:
            self.threaded = threaded

    def start(self, threaded=None):
        """Creates and starts the project."""
        if threaded is not None:
            self.threaded = threaded
        run = {'run': {'threaded': False}}
        self.project = project.project((self.desc),
          run, root_file=(self.project_file))
        self._run = self.project.run
        self._runner.start(self.threaded)

    def stop(self=None):
        """Stop the builder if it's running."""
        if not self:
            instance = getattr(Runner.instance(), 'builder', None)
            self = instance and instance()
            if not self:
                return
        else:
            self._runner.stop()
            if self.project:
                self.project.stop()
                self.project = None

    def clear(self):
        self.stop()
        super().clear()

    @property
    def is_running(self):
        """True if the Builder is currently running"""
        return self._runner.is_running

    @property
    def threaded(self):
        """
        True if the Builder is runs in a separate thread, false if the
        Builder blocks, waiting for the animation to end.
        """
        return self.desc.run.get('threaded', False)

    @threaded.setter
    def threaded(self, value):
        self.desc.run['threaded'] = bool(value)

    @staticmethod
    def simpixel(new=0, autoraise=True):
        """Open an instance of simpixel in the browser"""
        simpixel_driver.open_browser(new=new, autoraise=autoraise)

    @staticmethod
    def animations():
        """List all the existing animations"""
        animations.run(None)

    def __repr__(self):
        r = super().__repr__()
        if self.is_running:
            return 'Running ' + r
        else:
            return r

    def __iadd__(self, other):
        self.desc.update(other)
        return self

    def __add__(self, other):
        b = Builder()
        b += self
        b += other
        return b

    def __radd__(self, other):
        b = Builder()
        b += other
        b += self
        return b

    def __copy__(self):
        return self + {}

    def __deepcopy__(self, _):
        return self.__copy__()