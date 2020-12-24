# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/runner/runners/2.169.1/work/MetaWards/MetaWards/tests/../build/lib.macosx-10.14-x86_64-3.7/metawards/extractors/_extract_small.py
# Compiled at: 2020-05-10 15:00:16
# Size of source mod 2**32: 351 bytes
__all__ = ['extract_small']

def extract_small(**kwargs):
    """This extractor only extracts the 'small' default files,
       e.g. nothing that involves the incidence or prevalence
       matrices
    """
    from ._output_basic import output_basic
    from ._output_dispersal import output_dispersal
    return [
     output_basic, output_dispersal]