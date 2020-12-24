# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/bdgenomics/adam/models.py
# Compiled at: 2020-01-08 15:53:47
# Size of source mod 2**32: 1943 bytes
"""
======
models
======
.. currentmodule:: bdgenomics.adam.models
.. autosummary::
   :toctree: _generate/

   ReferenceRegion
"""

class ReferenceRegion:
    __doc__ = '\n    Represents a contiguous region of the reference genome.\n    '

    def __init__(self, referenceName, start, end):
        """
        Represents a contiguous region of the reference genome.

        :param referenceName The name of the sequence (chromosome) in the reference genome
        :param start The 0-based residue-coordinate for the start of the region
        :param end The 0-based residue-coordinate for the first residue <i>after</i> the start
        which is <i>not</i> in the region -- i.e. [start, end) define a 0-based
        half-open interval.
        """
        self.referenceName = referenceName
        self.start = start
        self.end = end

    def _toJava(self, jvm):
        """
        Converts to an org.bdgenomics.adam.models.ReferenceRegion

        Should not be called from user code.

        :param jvm: Py4j JVM handle.
        """
        return jvm.org.bdgenomics.adam.models.ReferenceRegion.fromGenomicRange(self.referenceName, self.start, self.end)