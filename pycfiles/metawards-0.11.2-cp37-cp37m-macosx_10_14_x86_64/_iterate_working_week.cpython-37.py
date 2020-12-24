# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/runner/runners/2.169.1/work/MetaWards/MetaWards/tests/../build/lib.macosx-10.14-x86_64-3.7/metawards/iterators/_iterate_working_week.py
# Compiled at: 2020-05-11 13:26:49
# Size of source mod 2**32: 1395 bytes
__all__ = ['iterate_working_week']
from ._iterate_weekday import iterate_weekday
from ._iterate_weekend import iterate_weekend
from .._population import Population

def iterate_working_week(population: Population, **kwargs):
    """This returns the default list of 'advance_XXX' functions that
       are called in sequence for each iteration of the model run.
       This iterator understands the concept of a traditional working week,
       namely Monday-Friday is a work day, while Saturday and
       Sunday are weekends

       Parameters
       ----------
       population: Population
         The population experiencing the outbreak. This includes
         information about the day and date of the outbreak

       Returns
       -------
       funcs: List[function]
         The list of functions that ```iterate``` will call in sequence
    """
    kwargs['population'] = population
    if population.date is None:
        day = population.day % 7
        is_weekend = day >= 5
    else:
        day = population.date.weekday()
        is_weekend = day >= 5
    if is_weekend:
        return iterate_weekend(**kwargs)
    return iterate_weekday(**kwargs)