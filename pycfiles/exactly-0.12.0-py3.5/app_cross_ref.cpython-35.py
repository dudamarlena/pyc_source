# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/definitions/cross_ref/app_cross_ref.py
# Compiled at: 2018-04-20 07:05:01
# Size of source mod 2**32: 713 bytes
"""The base class for cross refs for the Exactly application."""
from exactly_lib.util.textformat.structure.core import CrossReferenceTarget

class SeeAlsoTarget:
    __doc__ = '\n    A target that can be presented as a see-also item\n    '


class CrossReferenceId(CrossReferenceTarget, SeeAlsoTarget):
    __doc__ = '\n    A part of the help text that can be referred to.\n\n    The base class for all cross references used by Exactly.\n\n    Supports equality.\n    '

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return False
        return self._eq_object_of_same_type(other)

    def _eq_object_of_same_type(self, other):
        raise NotImplementedError('abstract method')