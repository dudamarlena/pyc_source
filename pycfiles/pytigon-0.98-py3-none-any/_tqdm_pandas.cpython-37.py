# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-6brxc_kc/tqdm/tqdm/_tqdm_pandas.py
# Compiled at: 2020-03-24 13:42:06
# Size of source mod 2**32: 1608 bytes
import sys
__author__ = 'github.com/casperdcl'
__all__ = ['tqdm_pandas']

def tqdm_pandas(tclass, *targs, **tkwargs):
    """
    Registers the given `tqdm` instance with
    `pandas.core.groupby.DataFrameGroupBy.progress_apply`.
    It will even close() the `tqdm` instance upon completion.

    Parameters
    ----------
    tclass  : tqdm class you want to use (eg, tqdm, tqdm_notebook, etc)
    targs and tkwargs  : arguments for the tqdm instance

    Examples
    --------
    >>> import pandas as pd
    >>> import numpy as np
    >>> from tqdm import tqdm, tqdm_pandas
    >>>
    >>> df = pd.DataFrame(np.random.randint(0, 100, (100000, 6)))
    >>> tqdm_pandas(tqdm, leave=True)  # can use tqdm_gui, optional kwargs, etc
    >>> # Now you can use `progress_apply` instead of `apply`
    >>> df.groupby(0).progress_apply(lambda x: x**2)

    References
    ----------
    https://stackoverflow.com/questions/18603270/
    progress-indicator-during-pandas-operations-python
    """
    from tqdm import TqdmDeprecationWarning
    if isinstance(tclass, type) or getattr(tclass, '__name__', '').startswith('tqdm_'):
        TqdmDeprecationWarning('Please use `tqdm.pandas(...)` instead of `tqdm_pandas(tqdm, ...)`.\n',
          fp_write=(getattr(tkwargs.get('file', None), 'write', sys.stderr.write)))
        (tclass.pandas)(*targs, **tkwargs)
    else:
        TqdmDeprecationWarning('Please use `tqdm.pandas(...)` instead of `tqdm_pandas(tqdm(...))`.\n',
          fp_write=(getattr(tclass.fp, 'write', sys.stderr.write)))
        type(tclass).pandas(deprecated_t=tclass)