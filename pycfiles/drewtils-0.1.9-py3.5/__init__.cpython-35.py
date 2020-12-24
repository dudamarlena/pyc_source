# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\drewtils\__init__.py
# Compiled at: 2017-12-04 21:59:04
# Size of source mod 2**32: 1656 bytes
import operator
from drewtils import parsers
__versions__ = '0.1.9'

def dfSubset(data, where):
    """
    Return a subset of the data given a series of conditions

    .. versionadded:: 0.1.9

    Parameters
    ----------
    data: :py:class:`pandas.DataFrame`:
        DataFrame to view
    where: str or list or tuple
        Conditions to apply.

    Notes
    -----

    If the argument is a string, it will be converted
    to a tuple for iteration. Items in iterable can be either a string
    or three-valued iterable of the following form::

        string: 'column operand target'
        iterable: ('column', 'operand', 'target')

    If the first-level item is a string, it will be split at spaces.
    Operands are string-representations of operators from the operator module,
    e.g.::

        'eq', 'ge', 'le', 'ne', 'gt', 'lt', 'contains'

    Returns
    -------
    view: :py:class:`pandas.DataFrame`:
        View into the data frame after successive slices

    See Also
    --------
    :py:mod:`operator`

    """
    view = data
    if isinstance(where, str):
        where = (
         where,)
    for item in where:
        if isinstance(item, str):
            cond = item.split()
        else:
            cond = item
        assert len(cond) == 3, 'Conditions should have three arguments, not like {}'.format(item)
        evalFunc = getattr(operator, cond[1])
        view = view[evalFunc(view[cond[0]], cond[2])]

    return view