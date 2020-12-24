# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ../../logomaker/src/examples.py
# Compiled at: 2019-04-28 20:05:59
import pandas as pd, os, gzip
from logomaker.src.error_handling import check, handle_errors
matrix_dir = os.path.dirname(os.path.abspath(__file__)) + '/../examples/matrices'
data_dir = os.path.dirname(os.path.abspath(__file__)) + '/../examples/datafiles'

@handle_errors
def list_example_matrices():
    """
    Return list of available matrices.
    """
    valid_matrices = [ ('.').join(name.split('.')[:-1]) for name in os.listdir(matrix_dir) if '.txt' in name
                     ]
    return valid_matrices


@handle_errors
def list_example_datafiles():
    """
    Return list of available data files.
    """
    valid_datafiles = [ name for name in os.listdir(data_dir) if len(name.split('.')) >= 2 and len(name.split('.')[0]) > 0
                      ]
    return valid_datafiles


@handle_errors
def get_example_matrix(name=None, print_description=True):
    """
    Returns an example matrix from which a logo can be made.

    parameters
    ----------

    name: (None or str)
        Name of example matrix.

    print_description: (bool)
        If true, a description of the example matrix will be printed

    returns
    -------

    df: (data frame)
        A data frame containing an example matrix.
    """
    valid_matrices = list_example_matrices()
    check(name in valid_matrices, 'Matrix "%s" not recognized. Please choose from: \n%s' % (
     name, ('\n').join([ repr(x) for x in valid_matrices ])))
    file_name = '%s/%s.txt' % (matrix_dir, name)
    assert os.path.isfile(file_name), 'File %s does not exist!' % file_name
    if print_description:
        print 'Description of example matrix "%s":' % name
        with open(file_name, 'r') as (f):
            lines = f.readlines()
            lines = [ l for l in lines if len(l) > 0 and l[0] == '#' ]
            description = ('').join(lines)
            print description
    return pd.read_csv(file_name, sep='\t', index_col=0, comment='#')


@handle_errors
def open_example_datafile(name=None, print_description=True):
    """
    Returns a file handle to an example dataset

    parameters
    ----------

    name: (None or str)
        Name of example matrix.

    print_description: (bool)
        If true, a description of the example matrix will be printed

    returns
    -------

    f: (file handle)
        A handle to the requested file
    """
    valid_datafiles = list_example_datafiles()
    check(name in valid_datafiles, 'Matrix "%s" not recognized. Please choose from: \n%s' % (
     name, ('\n').join([ repr(x) for x in valid_datafiles ])))
    file_name = '%s/%s' % (data_dir, name)
    assert os.path.isfile(file_name), 'File %s does not exist!' % file_name
    if print_description:
        print 'Description of example matrix "%s":' % name
        with open(file_name, 'r') as (f):
            lines = f.readlines()
            lines = [ l for l in lines if len(l) > 0 and l[0] == '#' ]
            description = ('').join(lines)
            print description
    if len(file_name) >= 3 and file_name[-3:] == '.gz':
        f = gzip.open(file_name, 'r')
    else:
        f = open(file_name, 'r')
    return f