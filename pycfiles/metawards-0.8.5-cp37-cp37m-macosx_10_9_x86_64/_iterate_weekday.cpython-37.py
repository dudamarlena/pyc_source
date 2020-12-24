# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/chris/GitHub/MetaWards/build/lib.macosx-10.9-x86_64-3.7/metawards/iterators/_iterate_weekday.py
# Compiled at: 2020-04-21 09:06:48
# Size of source mod 2**32: 1284 bytes
__all__ = ['iterate_weekday']

def iterate_weekday(nthreads: int=1, **kwargs):
    """This returns the default list of 'advance_XXX' functions that
       are called in sequence for each weekday iteration of the model run.

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
    if nthreads is None or nthreads == 1:
        from ._advance_infprob import advance_infprob_serial
        from ._advance_fixed import advance_fixed_serial
        from ._advance_play import advance_play_serial
        funcs = [advance_infprob_serial,
         advance_fixed_serial,
         advance_play_serial]
    else:
        from ._advance_infprob import advance_infprob_omp
        from ._advance_fixed import advance_fixed_omp
        from ._advance_play import advance_play_omp
        funcs = [
         advance_infprob_omp,
         advance_fixed_omp,
         advance_play_omp]
    return funcs