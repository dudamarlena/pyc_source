# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/bdgenomics/adam/stringency.py
# Compiled at: 2020-01-08 15:53:47
# Size of source mod 2**32: 1874 bytes
"""
==========
stringency
==========
.. currentmodule:: bdgenomics.adam.stringency
.. autosummary::
   :toctree: _generate/

   STRICT
   LENIENT
   SILENT
"""
STRICT = 2
LENIENT = 1
SILENT = 0

def _toJava(stringency, jvm):
    """
    Converts to an HTSJDK ValidationStringency enum.

    Should not be called from user code.

    :param bdgenomics.adam.stringency stringency: The desired stringency level.
    :param jvm: Py4j JVM handle.
    """
    if stringency is STRICT:
        return jvm.htsjdk.samtools.ValidationStringency.valueOf('STRICT')
    if stringency is LENIENT:
        return jvm.htsjdk.samtools.ValidationStringency.valueOf('LENIENT')
    if stringency is SILENT:
        return jvm.htsjdk.samtools.ValidationStringency.valueOf('SILENT')
    raise RuntimeError('Received %s. Stringency must be one of STRICT (%d), LENIENT (%d), or SILENT (%s).' % (stringency, STRICT, LENIENT, SILENT))