# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/MICA/bin/prep.py
# Compiled at: 2019-10-04 13:04:58
# Size of source mod 2**32: 2205 bytes
""" This script is responsible for pre-processing HDF5-format files for computation.
"""
import os, argparse, logging
from MICA.bin import utils

def main():
    """Handles arguments and calls the driver function"""
    head_description = 'Slice data, name parameters in input file, and generate data files with pairs of slices'
    parser = argparse.ArgumentParser(formatter_class=(argparse.RawDescriptionHelpFormatter), description=head_description)
    parser.add_argument('-i', '--input-file', metavar='STR', required=True, help='Input file')
    parser.add_argument('-o', '--output-file', metavar='STR', required=True, help='Output file name')
    parser.add_argument('-s', '--slice-unit', type=int, metavar='INT', required=True, help='Size of data slices')
    args = parser.parse_args()
    prep(args.input_file, args.output_file, args.slice_unit)


def prep(input_file, out_name, slice_unit):
    """Calls utility functions to preprocess input file

    Reads file into HDF5-format, adds parameters, slices data in file, generates several files with
    different combinations of slices

    Args:
        input_file (str): path to input text-file
        out_name   (str): common rootname of generated output files
        slice_unit (int): size of each slice of cell data in input text-file
    """
    logging.basicConfig(level=(logging.INFO))
    utils.read_file(input_file, out_name)
    h5_tmp = out_name + '.h5.tmp'
    utils.patch_file(h5_tmp, out_name)
    os.remove(h5_tmp)
    h5_whole = out_name + '.whole.h5'
    utils.slice_file(h5_whole, out_name, slice_unit)
    h5_sliced = out_name + '.sliced.h5'
    utils.calc_prep(h5_sliced, out_name)
    logging.info('MICA-prep step completed successfully.')


if __name__ == '__main__':
    main()