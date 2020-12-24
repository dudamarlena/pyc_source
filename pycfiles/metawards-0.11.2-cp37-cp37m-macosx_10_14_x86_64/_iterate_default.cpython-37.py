# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/runner/runners/2.169.1/work/MetaWards/MetaWards/tests/../build/lib.macosx-10.14-x86_64-3.7/metawards/iterators/_iterate_default.py
# Compiled at: 2020-05-11 13:26:49
# Size of source mod 2**32: 1380 bytes
from typing import List as _List
from utils._get_functions import MetaFunction
__all__ = [
 'iterate_default']

def iterate_default(stage: str, **kwargs) -> _List[MetaFunction]:
    """This returns the default list of 'advance_XXX' functions that
       are called in sequence for each iteration of the model run.
       This is the default iterator. It models every day as though
       it is a working day.

       Parameters
       ----------
       stage: str
         Which stage of the day is to be modelled

       Returns
       -------
       funcs: List[MetaFunction]
         The list of functions that will be called in sequence
    """
    if stage == 'initialise':
        from ._setup_imports import setup_seed_wards
        from ._advance_additional import setup_additional_seeds
        return [setup_seed_wards, setup_additional_seeds]
    if stage == 'setup':
        from ._advance_additional import advance_additional
        return [
         advance_additional]
    if stage == 'foi':
        from ._advance_foi import advance_foi
        from ._advance_recovery import advance_recovery
        return [
         advance_foi, advance_recovery]
    if stage == 'infect':
        from ._iterate_weekday import iterate_weekday
        return iterate_weekday(**kwargs)
    return []