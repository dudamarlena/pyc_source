# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/sisua/data/data_loader/centenarian.py
# Compiled at: 2019-09-16 06:27:59
# Size of source mod 2**32: 5416 bytes
import gzip, os, pickle, shutil, numpy as np
from odin.fuel import Dataset, MmapArrayWriter
from odin.stats import describe
from odin.utils import batching, ctext, get_file, one_hot, select_path
from odin.utils.crypto import decrypt_aes, md5_checksum
from sisua.data.path import DOWNLOAD_DIR, PREPROCESSED_BASE_DIR
from sisua.data.utils import remove_allzeros_columns, save_to_dataset
path = '/home/trung/bio_data/downloads/SuperCentenarian_original/01.UMI.txt.gz'
_URL = [
 'http://gerg.gsc.riken.jp/SC2018/01.UMI.txt.gz',
 'http://gerg.gsc.riken.jp/SC2018/02.UMI.lognorm.txt.gz',
 'http://gerg.gsc.riken.jp/SC2018/03.Cell.Barcodes.txt.gz',
 'http://gerg.gsc.riken.jp/SC2018/04.SC1.tar',
 'http://gerg.gsc.riken.jp/SC2018/05.SC2.tar']

def read_gzip_csv(path):
    data = []
    cell_id = None
    gene_id = None
    with gzip.open(path, mode='rb') as (f):
        for line in f:
            line = str(line, 'utf-8').strip().split('\t')
            data.append(line)

    cell_id = np.array(data[0])
    data = data[1:]
    gene_id = np.array([i[0] for i in data])
    data = np.array([i[1:] for i in data], dtype='float32').T
    return (data, cell_id, gene_id)


def read_centenarian(override=False, verbose=False):
    download_path = os.path.join(DOWNLOAD_DIR, 'SuperCentenarian_original')
    if not os.path.exists(download_path):
        os.mkdir(download_path)
    preprocessed_path = os.path.join(PREPROCESSED_BASE_DIR, 'SuperCentenarian_preprocessed')
    if override:
        if os.path.exists(preprocessed_path):
            shutil.rmtree(preprocessed_path)
    if not os.path.exists(preprocessed_path):
        os.mkdir(preprocessed_path)
    if not os.path.exists(os.path.join(preprocessed_path, 'X')):
        labels = get_file(fname=(os.path.basename(_URL[2])), origin=(_URL[2]),
          outdir=download_path,
          verbose=verbose)
        data = []
        with gzip.open(labels, mode='rb') as (f):
            for line in f:
                line = str(line, 'utf-8').strip().split('\t')
                assert line[1][:2] == line[2]
                data.append(line)

        labels = np.array(data)
        y_col = sorted(set(labels[:, 1]))
        y = one_hot(np.array([y_col.index(i) for i in labels[:, 1]]), len(y_col)).astype('float32')
        y_col = np.array(y_col)
        raw = get_file(fname=(os.path.basename(_URL[0])), origin=(_URL[0]),
          outdir=download_path,
          verbose=verbose)
        if verbose:
            print('Unzip and reading raw UMI ...')
        else:
            X_raw, cell_id1, gene_id1 = read_gzip_csv(raw)
            norm = get_file(fname=(os.path.basename(_URL[1])), origin=(_URL[1]),
              outdir=download_path,
              verbose=verbose)
            if verbose:
                print('Unzip and reading log-norm UMI ...')
            X_norm, cell_id2, gene_id2 = read_gzip_csv(norm)
            assert np.all(cell_id1 == cell_id2) and np.all(labels[:, 0] == cell_id1) and np.all(gene_id1 == gene_id2)
            if X_raw.shape[0] == X_norm.shape[0] == len(cell_id1):
                assert X_raw.shape[1] == X_norm.shape[1] == len(gene_id1)
        if verbose:
            print('Saving data to %s ...' % ctext(preprocessed_path, 'cyan'))
        save_to_dataset(preprocessed_path, X=X_raw,
          X_col=gene_id1,
          y=y,
          y_col=y_col,
          rowname=cell_id1,
          print_log=verbose)
        with MmapArrayWriter((os.path.join(preprocessed_path, 'X_log')), shape=(
         0, X_norm.shape[1]),
          dtype='float32',
          remove_exist=True) as (f):
            for s, e in batching(batch_size=2048, n=(X_norm.shape[0])):
                f.write(X_norm[s:e])

    ds = Dataset(preprocessed_path, read_only=True)
    return ds