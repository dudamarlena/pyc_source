# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/chris/GitHub/MetaWards/build/lib.macosx-10.9-x86_64-3.7/metawards/iterators/_iterate_default.py
# Compiled at: 2020-04-17 13:53:44
# Size of source mod 2**32: 1560 bytes
__all__ = ['iterate_default', 'iterator_needs_setup']
from ._iterate_core import iterate_core
from ._iterate_weekday import iterate_weekday

def iterator_needs_setup(iterator):
    """Return whether or not the passed iterator function has
       a "setup" argument, and thus needs to be setup before
       it can be used
    """
    import inspect
    return 'setup' in inspect.signature(iterator).parameters


def iterate_default(setup=False, **kwargs):
    """This returns the default list of 'advance_XXX' functions that
       are called in sequence for each iteration of the model run.
       This is the default iterator. It models every day as though
       it is a working day.

       Parameters
       ----------
       setup: bool
         Whether or not to return the functions used to setup the
         space and input for the advance_XXX functions returned by
         this iterator. This is called once at the start of a run
         to return the functions that must be called to setup the
         model

       Returns
       -------
       funcs: List[function]
         The list of functions that ```iterate``` will call in sequence
    """
    kwargs['setup'] = setup
    if setup:
        funcs = iterate_core(**kwargs)
        if iterator_needs_setup(iterate_weekday):
            funcs += iterate_weekday(**kwargs)
    else:
        funcs = iterate_core(**kwargs) + iterate_weekday(**kwargs)
    return funcs