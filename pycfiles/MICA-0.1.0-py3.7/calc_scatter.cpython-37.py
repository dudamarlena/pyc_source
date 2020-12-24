# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/MICA/bin/calc_scatter.py
# Compiled at: 2019-10-04 13:04:58
# Size of source mod 2**32: 1666 bytes
import pandas as pd, argparse
from MICA.bin import utils

def main():
    """Handles arguments and calls the driver function"""
    head_description = 'Calculate either one of these metrics in between two slices of data: mutual information, euclidean distance, pearson or spearman correlations.'
    parser = argparse.ArgumentParser(formatter_class=(argparse.RawDescriptionHelpFormatter), description=head_description)
    parser.add_argument('-i', '--input-file', metavar='STR', required=True, help='Input file')
    parser.add_argument('-m', '--metric', metavar='STR', required=True, help='Metric used in calculation')
    args = parser.parse_args()
    calc_scatter(args.input_file, args.metric.lower())


def calc_scatter(input_file, metric):
    """Calls calc_distance_mat utility function and calculates a metric in between cells that is chosen by the user

    Args:
        input_file (str): path to input HDF5-format file
        metric     (str): metric for calculation (mutual info, euclidean dist, pearson or spearman correlations
    """
    mat = pd.HDFStore(input_file)
    metrics = metric.lower()
    params = mat['params']
    mat1 = mat[params.loc[('key1', 0)]]
    mat2 = mat[params.loc[('key2', 0)]]
    mat.close()
    utils.calc_distance_mat(mat1, mat2, params, method=metrics)


if __name__ == '__main__':
    main()