# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/runner/runners/2.169.1/work/MetaWards/MetaWards/tests/../build/lib.macosx-10.14-x86_64-3.7/metawards/extractors/_extract_large.py
# Compiled at: 2020-05-11 13:26:49
# Size of source mod 2**32: 366 bytes
__all__ = ['extract_large']

def extract_large(**kwargs):
    """This extractor extracts the default files, plus the
       "large" files, e.g. S, E, I and R for each ward.
    """
    from ._output_wards_trajectory import output_wards_trajectory
    from ._extract_default import extract_default
    return extract_default(**kwargs) + [output_wards_trajectory]