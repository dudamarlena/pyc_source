# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/runner/runners/2.169.1/work/MetaWards/MetaWards/tests/../build/lib.macosx-10.14-x86_64-3.7/metawards/iterators/_iterate_weekend.py
# Compiled at: 2020-05-11 13:26:49
# Size of source mod 2**32: 786 bytes
__all__ = ['iterate_weekend']

def iterate_weekend(nthreads: int=1, **kwargs):
    """This returns the default list of 'advance_XXX' functions that
       are called in sequence for each weekend iteration of the model run.

       Parameters
       ----------
       nthreads: int
         The number of threads that will be used for each function.
         If this is 1, then the serial versions of the functions will
         be returned, else the parallel (OpenMP) versions will be
         returned

       Returns
       -------
       funcs: List[function]
         The list of functions that ```iterate``` will call in sequence
    """
    from ._advance_infprob import advance_infprob
    from ._advance_play import advance_play
    return [
     advance_infprob, advance_play]