# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/util/textformat/rendering/html/cross_ref.py
# Compiled at: 2017-12-07 08:04:08
# Size of source mod 2**32: 262 bytes
from exactly_lib.util.textformat.structure import core

class TargetRenderer:
    __doc__ = '\n    Abstract base class for rendering of a cross reference target.\n    '

    def apply(self, target: core.CrossReferenceTarget) -> str:
        raise NotImplementedError()