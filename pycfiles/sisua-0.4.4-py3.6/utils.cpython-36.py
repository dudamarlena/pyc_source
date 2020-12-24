# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/sisua/data/utils.py
# Compiled at: 2019-09-17 05:15:24
# Size of source mod 2**32: 6504 bytes
from __future__ import absolute_import, division, print_function
import base64, os, pickle, numpy as np
from scipy import sparse
from six import string_types
from odin.fuel import Dataset, MmapArrayWriter
from odin.utils import as_tuple, ctext

def _check_data(X, X_col, y, y_col, rowname):
    if not sparse.issparse(X):
        if not np.min(X) >= 0:
            raise AssertionError('Only support non-negative value for X')
    else:
        assert X_col.ndim == 1 and len(X_col) == X.shape[1]
        assert rowname.ndim == 1 and len(rowname) == X.shape[0]
    if y is not None and len(y.shape) > 0 and y.shape[1] != 0:
        if not sparse.issparse(y):
            if not np.min(y) >= 0:
                raise AssertionError('Only support non-negative value for y')
        else:
            assert X.ndim == 2 and y.ndim == 2, 'Only support matrix for `X` and `y`'
            assert X.shape[0] == y.shape[0], 'Number of sample mismatch `X=%s` and `y=%s`' % (X.shape, y.shape)
        if not (y_col.ndim == 1 and len(y_col) == y.shape[1]):
            raise AssertionError


def read_gzip_csv(path):
    import gzip
    with gzip.open(path, 'rb') as (file_obj):
        data = []
        for line in file_obj:
            line = str(line, 'utf-8').strip()
            line = line.split(',')
            data.append(line)

        data = np.array(data)
        return data


_protein_name = {'PD-L1;CD274':'CD274', 
 'PECAM;CD31':'CD31', 
 'CD26;Adenosine':'CD26', 
 'CD366;tim3':'CD366', 
 'MHCII;HLA-DR':'MHCII', 
 'IL7Ralpha;CD127':'CD127', 
 'PD-1':'PD-1', 
 'PD1':'PD1', 
 'B220;CD45R':'CD45R', 
 'Ox40;CD134':'CD134', 
 'CD8a':'CD8', 
 'CD8A':'CD8', 
 'CD4 T cells':'CD4', 
 'CD8 T cells':'CD8'}

def standardize_protein_name(name):
    """ standardize """
    assert isinstance(name, string_types), 'Protein name must be string types'
    name = name.replace('-TotalSeqB', '')
    name = name.strip()
    if name in _protein_name:
        name = _protein_name[name]
    return name


def get_gene_id2name():
    """ Return the mapping from gene identifier to gene symbol (i.e. name)
  for PBMC 8k data
  """
    from odin.utils import get_file
    from sisua.data.path import DOWNLOAD_DIR
    url = base64.decodebytes(b'aHR0cHM6Ly9haS1kYXRhc2V0cy5zMy5hbWF6b25hd3MuY29tL2dlbmVfaWQybmFtZS5wa2w=\n')
    url = str(url, 'utf-8')
    get_file('gene_id2name.pkl', url, DOWNLOAD_DIR)
    with open(os.path.join(DOWNLOAD_DIR, 'gene_id2name.pkl'), 'rb') as (f):
        return pickle.load(f)


def remove_allzeros_columns(matrix, colname, print_log=True):
    """ Remove all zero columns from both the matrix and column name vector

  Return
  ------
  matrix : [n_samples, n_genes]
  column_name : [n_genes]
  """
    assert matrix.ndim == 2
    orig_shape = matrix.shape
    nonzero_col = np.sum(matrix, axis=0) > 1
    matrix = matrix[:, nonzero_col]
    colname = colname[nonzero_col]
    if print_log:
        print('Filtering %d all-zero columns from data: %s -> %s ...' % (
         len(nonzero_col) - np.sum(nonzero_col), str(orig_shape),
         str(matrix.shape)))
    return (
     matrix, colname)


def validating_dataset(path):
    if isinstance(path, Dataset):
        ds = path
    else:
        if isinstance(path, string_types):
            ds = Dataset(path, read_only=True)
        else:
            if not 'X' in ds:
                raise AssertionError('`X` (n_samples, n_genes) must be stored at path: %s' % ds.path)
            elif not 'X_col' in ds:
                raise AssertionError('`X_col` (n_genes,) must be stored at path: %s' % ds.path)
            assert 'X_row' in ds, '`X_row` (n_samples,) must be stored at path: %s' % ds.path
        if 'y' in ds:
            if not 'y' in ds:
                raise AssertionError('`y` (n_samples, n_protein) must be stored at path: %s' % ds.path)
            elif not 'y_col' in ds:
                raise AssertionError('`y_col` (n_protein,) must be stored at path: %s' % ds.path)
            y, y_col = ds['y'], ds['y_col']
        else:
            y, y_col = (None, None)
    X, X_col, rowname = ds['X'], ds['X_col'], ds['X_row']
    _check_data(X, X_col, y, y_col, rowname)


def save_to_dataset(path, X, X_col=None, y=None, y_col=None, rowname=None, print_log=True):
    """
  path : output folder path
  X : (n_samples, n_genes) gene expression matrix
  X_col : (n_genes,) name of each gene
  y : (n_samples, n_proteins) protein marker level matrix
  y_col : (n_proteins) name of each protein
  rowname : (n_samples,) name of cells (i.e. the sample)
  print_log : bool (default: True)
  """
    _check_data(X, X_col, y, y_col, rowname)
    assert os.path.isdir(path), "'%s' must be path to a folder" % path
    if print_log:
        print('Saving data to %s ...' % ctext(path, 'cyan'))
    else:
        if sparse.issparse(X):
            with open(os.path.join(path, 'X'), 'wb') as (f):
                pickle.dump(X, f)
        else:
            with MmapArrayWriter(path=(os.path.join(path, 'X')), dtype='float32',
              shape=(
             0, X.shape[1]),
              remove_exist=True) as (out):
                out.write(X)
        if X_col is not None:
            with open(os.path.join(path, 'X_col'), 'wb') as (f):
                pickle.dump(X_col, f)
        if y is not None:
            if len(y.shape) > 0:
                if y.shape[1] != 0:
                    if sparse.issparse(y):
                        with open(os.path.join(path, 'y'), 'wb') as (f):
                            pickle.dump(y, f)
                    else:
                        with MmapArrayWriter(path=(os.path.join(path, 'y')), dtype='float32',
                          shape=(
                         0, y.shape[1]),
                          remove_exist=True) as (out):
                            out.write(y)
                    with open(os.path.join(path, 'y_col'), 'wb') as (f):
                        pickle.dump(y_col, f)
    if rowname is not None:
        with open(os.path.join(path, 'X_row'), 'wb') as (f):
            pickle.dump(rowname, f)