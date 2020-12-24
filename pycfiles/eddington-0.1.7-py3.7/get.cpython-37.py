# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/eddington/input/get.py
# Compiled at: 2020-04-04 13:10:47
# Size of source mod 2**32: 1287 bytes
from pathlib import Path
from eddington.input.csv import read_data_from_csv
from eddington.input.excel import read_data_from_excel
from eddington.input.random import random_data
from eddington.input.reduction import reduce_data

def get_data_dict_from_args(func, args):
    if args.random_data:
        return random_data(func=func,
          actual_a=(args.actual_a),
          xmin=(args.xmin),
          xmax=(args.xmax),
          measurements=(args.measurements),
          xsigma=(args.xsigma),
          ysigma=(args.ysigma),
          min_coeff=(args.min_coeff),
          max_coeff=(args.max_coeff))
    data_frame = get_data_from_file(args)
    if data_frame is not None:
        return reduce_data(data_dict=data_frame,
          x_column=(args.x_column),
          xerr_column=(args.xerr_column),
          y_column=(args.y_column),
          yerr_column=(args.yerr_column))


def get_data_from_file(args):
    if args.csv_data is not None:
        return read_data_from_csv(filepath=(Path(args.csv_data)))
    if args.excel_data is not None:
        file_path = Path(args.excel_data[0])
        sheet_name = args.excel_data[1]
        return read_data_from_excel(filepath=file_path, sheet=sheet_name)