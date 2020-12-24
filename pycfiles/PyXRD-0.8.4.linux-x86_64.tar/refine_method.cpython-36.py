# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pyxrd/refinement/refine_method.py
# Compiled at: 2020-03-07 03:51:50
# Size of source mod 2**32: 1900 bytes
import logging
logger = logging.getLogger(__name__)
from .refine_method_meta import RefineMethodMeta
from .refine_async_helper import RefineAsyncHelper
from pyxrd.calculations.mixture import get_optimized_residual

class RefineMethod(RefineAsyncHelper, metaclass=RefineMethodMeta):
    __doc__ = '\n        The `RefineMethod` class is the base class for refinement methods.\n        Sub-classes will be registered in the metaclass.\n    '
    name = 'Name of the algorithm'
    description = 'A slightly longer explanation of algorithm'
    index = -1
    disabled = True
    residual_callback = property(fget=(lambda *s: get_optimized_residual))

    def __call__(self, refiner, stop=None, **kwargs):
        self._stop = stop
        options = self.get_options()
        for arg in self.options:
            options[arg] = kwargs.get(arg, getattr(self, arg))

        return (self.run)(refiner, **options)

    def run(self, refiner, **kwargs):
        raise NotImplementedError('The run method of RefineRun should be implemented by sub-classes...')

    def get_options(self):
        """ Returns a dict containing the option attribute names as keys and
        their values as values """
        return {name:getattr(self, name) for name in self.options}