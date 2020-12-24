# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/runner/runners/2.169.1/work/MetaWards/MetaWards/tests/../build/lib.macosx-10.14-x86_64-3.7/metawards/mixers/_mix_evenly.py
# Compiled at: 2020-05-11 13:26:49
# Size of source mod 2**32: 471 bytes
__all__ = ['mix_evenly']

def mix_evenly(stage: str, **kwargs):
    """This mixer will evenly mix all demographics. This should be
       equivalent to a null model, and produce similar results
       as if the population was all in a single demographic
    """
    if stage == 'foi':
        from ._merge_evenly import merge_evenly
        return [
         merge_evenly]
    from ._mix_default import mix_default
    return mix_default(stage=stage, **kwargs)