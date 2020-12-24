# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/eddington/input/reduction.py
# Compiled at: 2020-04-04 13:10:47
# Size of source mod 2**32: 1465 bytes
from eddington.consts import DEFAULT_X_COLUMN
from collections import OrderedDict, defaultdict
from eddington.exceptions import ColumnsDuplicationError

def reduce_data(data_dict, x_column=DEFAULT_X_COLUMN, xerr_column=None, y_column=None, yerr_column=None):
    x_column, x = get_column(data_dict, x_column)
    xerr_column, xerr = get_column(data_dict, xerr_column, previous_column=x_column)
    y_column, y = get_column(data_dict, y_column, previous_column=xerr_column)
    yerr_column, yerr = get_column(data_dict, yerr_column, previous_column=y_column)
    validate_no_duplications(x=x_column,
      xerr=xerr_column,
      y=y_column,
      yerr=yerr_column)
    return OrderedDict([
     (
      x_column, x), (xerr_column, xerr), (y_column, y), (yerr_column, yerr)])


def get_column(data, column, previous_column=None):
    items = list(data.items())
    if column is None:
        if previous_column is not None:
            keys = list(data.keys())
            previous_index = keys.index(previous_column)
            return items[(previous_index + 1)]
    try:
        return items[(int(column) - 1)]
    except ValueError:
        return (
         column, data[column])


def validate_no_duplications(**kwargs):
    v = defaultdict(list)
    for key, value in sorted(kwargs.items()):
        v[value].append(key)

    duplicate = [value for key, value in v.items() if len(value) != 1]
    if len(duplicate) != 0:
        raise ColumnsDuplicationError(duplicate[0])