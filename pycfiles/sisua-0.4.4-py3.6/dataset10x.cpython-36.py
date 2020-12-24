# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/sisua/data/data_loader/dataset10x.py
# Compiled at: 2019-09-17 05:21:50
# Size of source mod 2**32: 7131 bytes
from __future__ import absolute_import, division, print_function
import gzip, os, pickle, shutil, tarfile
from typing import Tuple
import numpy as np, pandas as pd
from scipy.io import mmread
from scipy.sparse import csr_matrix, issparse
from odin.fuel import Dataset
from odin.utils import batching, ctext, get_file, is_gzip_file, select_path
from sisua.data.path import DOWNLOAD_DIR, PREPROCESSED_BASE_DIR
from sisua.data.utils import remove_allzeros_columns, save_to_dataset
available_datasets = {'1.1.0':[
  'frozen_pbmc_donor_a',
  'frozen_pbmc_donor_b',
  'frozen_pbmc_donor_c',
  'fresh_68k_pbmc_donor_a',
  'cd14_monocytes',
  'b_cells',
  'cd34',
  'cd56_nk',
  'cd4_t_helper',
  'regulatory_t',
  'naive_t',
  'memory_t',
  'cytotoxic_t',
  'naive_cytotoxic'], 
 '2.1.0':[
  'pbmc8k', 'pbmc4k', 't_3k', 't_4k', 'neuron_9k'], 
 '3.0.0':[
  'pbmc_1k_protein_v3',
  'pbmc_10k_protein_v3',
  'malt_10k_protein_v3',
  'pbmc_1k_v2',
  'pbmc_1k_v3',
  'pbmc_10k_v3',
  'hgmm_1k_v2',
  'hgmm_1k_v3',
  'hgmm_5k_v3',
  'hgmm_10k_v3',
  'neuron_1k_v2',
  'neuron_1k_v3',
  'neuron_10k_v3',
  'heart_1k_v2',
  'heart_1k_v3',
  'heart_10k_v3'], 
 '3.1.0':[
  '5k_pbmc_protein_v3', '5k_pbmc_protein_v3_nextgem']}
dataset_to_group = dict([(dataset_name, group) for group, list_datasets in available_datasets.items() for dataset_name in list_datasets])
group_to_url_skeleton = {'1.1.0':'http://cf.10xgenomics.com/samples/cell-exp/{}/{}/{}_{}_gene_bc_matrices.tar.gz', 
 '2.1.0':'http://cf.10xgenomics.com/samples/cell-exp/{}/{}/{}_{}_gene_bc_matrices.tar.gz', 
 '3.0.0':'http://cf.10xgenomics.com/samples/cell-exp/{}/{}/{}_{}_feature_bc_matrix.tar.gz', 
 '3.1.0':'http://cf.10xgenomics.com/samples/cell-exp/{}/{}/{}_{}_feature_bc_matrix.tar.gz'}
available_specification = [
 'filtered', 'raw']

def read_dataset10x_cellexp(name, spec, override=False, verbose=False):
    if not spec in available_specification:
        raise AssertionError("Unknown specification '%s'" % spec)
    else:
        if name == 'cellvdj':
            url = 'http://cf.10xgenomics.com/samples/cell-vdj/3.0.2/vdj_v1_hs_aggregated_donor1/vdj_v1_hs_aggregated_donor1_%s_feature_bc_matrix.tar.gz'
            url = url % spec
        else:
            group = dataset_to_group[name]
            url_skeleton = group_to_url_skeleton[group]
            url = url_skeleton.format(group, name, name, spec)
        filename = os.path.basename(url)
        download_path = os.path.join(DOWNLOAD_DIR, name)
        if not os.path.exists(download_path):
            os.mkdir(download_path)
        preprocessed_path = os.path.join(PREPROCESSED_BASE_DIR, '%s_%s_preprocessed' % (name, spec))
        if override:
            if os.path.exists(preprocessed_path):
                if verbose:
                    print('Overriding path: %s' % preprocessed_path)
                shutil.rmtree(preprocessed_path)
        if not os.path.exists(preprocessed_path):
            os.mkdir(preprocessed_path)
        if not os.path.exists(os.path.join(preprocessed_path, 'X')):
            path = get_file(fname=filename, origin=url,
              outdir=download_path,
              verbose=(bool(verbose)))
            if not tarfile.is_tarfile(path):
                raise RuntimeError('Expecting tarfile but received: %s' % path)
            contents = {}
            with tarfile.open(path, mode='r:gz') as (f):
                for info in f:
                    if info.isfile():
                        name = info.name
                        if verbose:
                            print("Extracting '%s' size %.2f(MB) ..." % (
                             name, info.size / 1024.0 / 1024.0))
                        data = f.extractfile(name)
                        if is_gzip_file(data):
                            data = gzip.open(data, mode='rb')
                        name = os.path.basename(name).split('.')[0]
                        if name == 'barcodes':
                            data = np.array([str(line, 'utf-8')[:-1] for line in data])
                        else:
                            if name == 'features' or name == 'genes':
                                _ = []
                                for line in data:
                                    line = str(line, 'utf-8')[:-1].split('\t')
                                    _.append(line)

                                data = np.array(_)
                            else:
                                if name == 'matrix':
                                    data = mmread(data)
                                else:
                                    raise RuntimeError("Unknown downloaded file '%s', something changed from 10xGenomics." % name)
                        contents[name] = data

            X_row = contents['barcodes']
            X_col = contents['features'] if 'features' in contents else contents['genes']
            X = contents['matrix'].T
            if not isinstance(X, csr_matrix):
                if hasattr(X, 'tocsr'):
                    X = X.tocsr()
            X = X.astype('float32')
            assert X.shape[0] == X_row.shape[0] and X.shape[1] == X_col.shape[0]
            prot_ids = []
            gene_ids = []
            if X_col.shape[1] == 3:
                for idx, row in enumerate(X_col):
                    if row[(-1)] == 'Antibody Capture':
                        prot_ids.append(idx)
                    else:
                        if row[(-1)] == 'Gene Expression':
                            gene_ids.append(idx)
                        else:
                            raise ValueError('Unknown feature type: %s' % str(row))

            else:
                gene_ids = slice(None, None)
            y = X[:, prot_ids]
            y_col = X_col[prot_ids][:, 0]
            y_col_name = X_col[prot_ids][:, 1]
            X = X[:, gene_ids]
            X_col_name = X_col[gene_ids][:, 1]
            X_col = X_col[gene_ids][:, 0]
            if len(X_row) < 60000:
                if verbose:
                    print('Less than 60000 samples, convert all sparse matrices to dense ...')
                else:
                    if issparse(X):
                        X = X.todense()
                    if issparse(y):
                        y = y.todense()
            save_to_dataset(preprocessed_path, X=X,
              X_col=X_col,
              y=y,
              y_col=y_col,
              rowname=X_row,
              print_log=verbose)
            with open(os.path.join(preprocessed_path, 'X_col_name'), 'wb') as (f):
                pickle.dump(X_col_name, f)
            if len(y_col_name) > 0:
                with open(os.path.join(preprocessed_path, 'y_col_name'), 'wb') as (f):
                    pickle.dump(y_col_name, f)
    ds = Dataset(preprocessed_path, read_only=True)
    return ds