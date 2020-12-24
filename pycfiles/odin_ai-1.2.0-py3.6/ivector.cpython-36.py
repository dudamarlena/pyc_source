# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/odin/ml/ivector.py
# Compiled at: 2019-08-13 03:54:01
# Size of source mod 2**32: 17874 bytes
from __future__ import absolute_import, division, print_function
import os, pickle, numpy as np
from odin.fuel import MmapArray, MmapArrayWriter
from odin.ml.base import BaseEstimator, DensityMixin, TransformerMixin
from odin.ml.gmm_tmat import GMM, Tmatrix, _split_jobs
from odin.utils import Progbar, UnitTimer, batching, crypto, ctext, is_primitives, mpi, uuid

def _extract_zero_and_first_stats(X, sad, indices, gmm, z_path, f_path, name_path):
    n_samples = X.shape[0]
    if indices is None:
        if os.path.exists(z_path):
            os.remove(z_path)
        if os.path.exists(f_path):
            os.remove(f_path)
        Z = MmapArrayWriter(path=z_path, dtype='float32',
          shape=(
         n_samples, gmm.nmix),
          remove_exist=True)
        F = MmapArrayWriter(path=f_path, dtype='float32',
          shape=(
         n_samples, gmm.feat_dim * gmm.nmix),
          remove_exist=True)
        jobs, _ = _split_jobs(n_samples, ncpu=(mpi.cpu_count()),
          device='cpu',
          gpu_factor=1)

        def map_transform(start_end):
            start, end = start_end
            for i in range(start, end):
                if sad is not None and not bool(sad[i]):
                    yield (None, None, None)
                else:
                    z, f = gmm.transform((X[i][np.newaxis, :]), zero=True,
                      first=True,
                      device='cpu')
                    yield (i, z, f)

        prog = Progbar(target=n_samples, print_report=True,
          print_summary=False,
          name='Extracting zero and first order statistics')
        for i, z, f in mpi.MPI(jobs, map_transform, ncpu=None, batch=1):
            if i is not None:
                Z[i] = z
                F[i] = f
            prog.add(1)

        Z.flush()
        F.flush()
        Z.close()
        F.close()
    else:
        gmm.transform_to_disk(X, indices=indices,
          sad=sad,
          pathZ=z_path,
          pathF=f_path,
          name_path=name_path,
          dtype='float32',
          device=None,
          ncpu=None,
          override=True)


class Ivector(DensityMixin, BaseEstimator, TransformerMixin):
    __doc__ = ' Ivector extraction using GMM and T-matrix '

    def __init__(self, path, nmix=None, tv_dim=None, nmix_start=1, niter_gmm=16, niter_tmat=16, allow_rollback=True, exit_on_error=False, downsample=1, stochastic_downsample=True, device='gpu', ncpu=1, gpu_factor_gmm=80, gpu_factor_tmat=3, dtype='float32', seed=1234, name=None):
        super(Ivector, self).__init__()
        for key, val in locals().items():
            if key in ('self', 'path', 'seed'):
                pass
            else:
                setattr(self, key, val)

        self._rand = np.random.RandomState(seed=seed)
        path = str(path)
        if not os.path.exists(path):
            os.mkdir(path)
        else:
            if not os.path.isdir(path):
                raise ValueError("Path to '%s' is not a directory" % str(path))
        self._path = path
        self._gmm = None
        self._tmat = None

    @property
    def gmm(self):
        if self._gmm is None:
            if os.path.exists(self.gmm_path):
                with open(self.gmm_path, 'rb') as (f):
                    self._gmm = pickle.load(f)
                assert self._gmm.nmix == self.nmix, "Require GMM with %d components, but found %s, at path: '%s'" % (
                 self.nmix, str(self._gmm), self.gmm_path)
            else:
                self._gmm = GMM(nmix=(self.nmix), niter=(self.niter_gmm),
                  dtype=(self.dtype),
                  downsample=(self.downsample),
                  stochastic_downsample=(self.stochastic_downsample),
                  device=(self.device),
                  ncpu=(self.ncpu),
                  gpu_factor=(self.gpu_factor_gmm),
                  seed=1234,
                  path=(self.gmm_path),
                  name=('IvecGMM_%s' % (self.name if self.name is not None else str(self._rand.randint(1000000000.0)))))
        return self._gmm

    @property
    def tmat(self):
        if self._tmat is None:
            if os.path.exists(self.tmat_path):
                with open(self.tmat_path, 'rb') as (f):
                    self._tmat = pickle.load(f)
                assert self._tmat.tv_dim == self.tv_dim, "Require T-matrix with %d dimensions, but found %s, at path: '%s'" % (
                 self.tv_dim, str(self._tmat), self.tmat_path)
            else:
                self._tmat = Tmatrix(tv_dim=(self.tv_dim), gmm=(self.gmm),
                  niter=(self.niter_tmat),
                  dtype=(self.dtype),
                  device=(self.device),
                  ncpu=(self.ncpu),
                  gpu_factor=(self.gpu_factor_tmat),
                  cache_path='/tmp',
                  seed=1234,
                  path=(self.tmat_path),
                  name=('IvecTmat_%s' % (self.name if self.name is not None else str(self._rand.randint(1000000000.0)))))
        return self._tmat

    @property
    def path(self):
        return self._path

    @property
    def gmm_path(self):
        return os.path.join(self.path, 'gmm.pkl')

    @property
    def tmat_path(self):
        return os.path.join(self.path, 'tmat.pkl')

    @property
    def z_path(self):
        """ Path to zero-th order statistics of the training data"""
        return os.path.join(self.path, 'zstat_train')

    @property
    def f_path(self):
        """ Path to first order statistics of the training data """
        return os.path.join(self.path, 'fstat_train')

    @property
    def ivec_path(self):
        """ Path to first order statistics of the training data """
        return os.path.join(self.path, 'ivec_train')

    @property
    def name_path(self):
        """ In case indices is given during training, the order of
    processed files is store at this path """
        return os.path.join(self.path, 'name_train')

    @property
    def feat_dim(self):
        return self.gmm.feat_dim

    @property
    def is_gmm_fitted(self):
        return self.gmm.is_fitted

    @property
    def is_tmat_fitted(self):
        return self.is_gmm_fitted and self.tmat.is_fitted

    @property
    def is_fitted(self):
        return self.is_gmm_fitted and self.is_tmat_fitted

    def get_z_path(self, name=None):
        """ Return the path the zero-order statistics
    according to the given name as identification during
    `Ivector.transform`
    If name is None, return `Ivector.z_path`
    """
        if name is None:
            return self.z_path
        else:
            return os.path.join(self.path, 'zstat_%s' % name)

    def get_f_path(self, name):
        """ Return the path the first-order statistics
    according to the given name as identification during
    `Ivector.transform`
    If name is None, return `Ivector.f_path`
    """
        if name is None:
            return self.f_path
        else:
            return os.path.join(self.path, 'fstat_%s' % name)

    def get_i_path(self, name):
        """ Return the path the extracted i-vectors
    according to the given name as identification during
    `Ivector.transform`
    If name is None, return `Ivector.ivec_path`
    """
        if name is None:
            return self.ivec_path
        else:
            return os.path.join(self.path, 'ivec_%s' % name)

    def get_name_path(self, name):
        """ Return the path of the name list if indices is used
    according to the given name as identification during
    `Ivector.transform`
    If name is None, return `Ivector.name_path`
    """
        if name is None:
            return self.name_path
        else:
            return os.path.join(self.path, 'name_%s' % name)

    def fit(self, X, indices=None, sad=None, refit_gmm=False, refit_tmat=False, extract_ivecs=False, keep_stats=False):
        """
    Parameters
    ----------
    X : ndarray
      Training data [n_samples, n_features]

    indices : {Mapping, tuple, list}
      in case the data is given by a list of files, `indices`
      act as file indicator mapping from
      'file_name' -> (start_index_in_X, end_index_in_X)
      This mapping can be provided by a dictionary, or list of
      tuple.
      Note: the order provided in indices will be preserved

    sad : ndarray
      inspired by the "Speech Activity Detection" (SAD) indexing,
      this array is indicator of which samples will be taken into
      training; the shape should be [n_samples,] or [n_samples, 1]

    refit_gmm : bool
      if True, re-fit the GMM even though it is fitted,
      consequently, the T-matrix will be re-fitted

    refit_tmat : bool
      if True, re-fit the T-matrix even though it is fitted

    extract_ivecs : bool
      if True, extract the i-vector for training data

    keep_stats : bool
      if True, keep the zero and first order statistics.
      The first order statistics could consume huge amount
      of disk space. Otherwise, they are deleted after training
    """
        new_gmm = not self.gmm.is_fitted or refit_gmm
        if os.path.exists(self.z_path):
            Z = MmapArray(self.z_path)
            if Z.shape[0] == 0:
                os.remove(self.z_path)
            Z.close()
        if os.path.exists(self.f_path):
            F = MmapArray(self.f_path)
            if F.shape[0] == 0:
                os.remove(self.f_path)
            F.close()
        if os.path.exists(self.ivec_path):
            ivec = MmapArray(self.ivec_path)
            if ivec.shape[0] == 0:
                os.remove(self.ivec_path)
            ivec.close()
        if new_gmm:
            input_data = [
             X]
            if sad is not None:
                input_data.append(sad)
            if indices is not None:
                input_data.append(indices)
            self.gmm.fit(input_data)
        else:
            new_tmat = not self.tmat.is_fitted or new_gmm or refit_tmat
            new_ivec = extract_ivecs and (new_tmat or not os.path.exists(self.ivec_path))
            if not new_gmm:
                if os.path.exists(self.z_path):
                    if os.path.exists(self.f_path):
                        new_stats = False
            new_stats = new_gmm or new_tmat or new_ivec
        if new_stats:
            _extract_zero_and_first_stats(X=X, sad=sad,
              indices=indices,
              gmm=(self.gmm),
              z_path=(self.z_path),
              f_path=(self.f_path),
              name_path=(self.name_path))
        if new_tmat or new_ivec:
            Z = MmapArray(path=(self.z_path))
            F = MmapArray(path=(self.f_path))
            if new_tmat:
                self.tmat.fit((Z, F))
            if new_ivec:
                self.tmat.transform_to_disk(path=(self.ivec_path), Z=Z,
                  F=F,
                  dtype='float32',
                  device='gpu',
                  override=True)
            Z.close()
            F.close()
        if not keep_stats:
            if os.path.exists(self.z_path):
                os.remove(self.z_path)
            if os.path.exists(self.f_path):
                os.remove(self.f_path)
        return self

    def transform(self, X, indices=None, sad=None, save_ivecs=False, keep_stats=False, name=None):
        """
    Parameters
    ----------
    X : ndarray
      Training data [n_samples, n_features]
    indices : {Mapping, tuple, list}
      in case the data is given by a list of files, `indices`
      act as file indicator mapping from
      'file_name' -> (start_index_in_X, end_index_in_X)
      This mapping can be provided by a dictionary, or list of
      tuple.
    sad : ndarray
      inspired by the "Speech Activity Detection" (SAD) indexing,
      this array is indicator of which samples will be taken into
      training; the shape should be [n_samples,] or [n_samples, 1]
    save_ivecs : bool
      if True, save extracted i-vectors to disk at path `ivec_[name]`
      if False, return directly the i-vectors without saving

    keep_stats : bool
      if True, keep the zero and first order statistics.
      The first order statistics could consume huge amount
      of disk space. Otherwise, they are deleted after training
    name : {None, str}
      identity of the i-vectors (for re-using in future).
      If None, a random name is used
    """
        if not self.is_fitted:
            raise ValueError('Ivector has not been fitted, call Ivector.fit(...) first')
        else:
            n_files = X.shape[0] if indices is None else len(indices)
            if name is None:
                name = uuid(length=8)
            else:
                name = str(name)
            z_path = self.get_z_path(name)
            f_path = self.get_f_path(name)
            if save_ivecs:
                i_path = self.get_i_path(name)
            else:
                i_path = None
        name_path = self.get_name_path(name)
        if i_path is not None and os.path.exists(i_path):
            ivec = MmapArray(path=i_path)
            assert ivec.shape[0] == n_files and ivec.shape[1] == self.tv_dim, "Need i-vectors for %d files, found exists data at path:'%s' with shape:%s" % (
             n_files, i_path, ivec.shape)
            return ivec
        else:
            if os.path.exists(z_path):
                if os.path.exists(f_path):
                    pass
                else:
                    if os.path.exists(z_path):
                        os.remove(z_path)
                    else:
                        if os.path.exists(f_path):
                            os.remove(f_path)
                        if os.path.exists(name_path):
                            os.remove(name_path)
                    _extract_zero_and_first_stats(X=X, sad=sad,
                      indices=indices,
                      gmm=(self.gmm),
                      z_path=z_path,
                      f_path=f_path,
                      name_path=name_path)
            else:
                Z = MmapArray(path=z_path)
                F = MmapArray(path=f_path)
                ivec = self.tmat.transform_to_disk(path=i_path, Z=Z, F=F, dtype='float32')
                Z.close()
                F.close()
                if not keep_stats:
                    if os.path.exists(z_path):
                        os.remove(z_path)
                    if os.path.exists(f_path):
                        os.remove(f_path)
                else:
                    print('Zero-order stats saved at:', ctext(z_path, 'cyan'))
                    print('First-order stats saved at:', ctext(f_path, 'cyan'))
            return ivec

    def __str__(self):
        s = ''
        s += ctext('<Ivector ', 'yellow')
        s += 'GMM:%s ' % self.is_gmm_fitted
        s += 'Tmat:%s\n' % self.is_tmat_fitted
        if os.path.exists(self.path) and len(os.listdir(self.path)) > 0:
            s += '  %s: ' % ctext('model', 'cyan')
            s += ', '.join(['"%s"' % f for f in sorted(os.listdir(self.path)) if 'zstat' not in f if 'fstat' not in f if 'ivec' not in f if 'name_' not in f])
            s += '\n'
            s += '  %s: ' % ctext('Z-stats', 'cyan')
            s += ', '.join(['"%s"' % f for f in sorted(os.listdir(self.path)) if 'zstat' in f])
            s += '\n'
            s += '  %s: ' % ctext('F-stats', 'cyan')
            s += ', '.join(['"%s"' % f for f in sorted(os.listdir(self.path)) if 'fstat' in f])
            s += '\n'
            s += '  %s: ' % ctext('ivec', 'cyan')
            s += ', '.join(['"%s"' % f for f in sorted(os.listdir(self.path)) if 'ivec' in f])
            s += '\n'
            s += '  %s: ' % ctext('name-list', 'cyan')
            s += ', '.join(['"%s"' % f for f in sorted(os.listdir(self.path)) if 'name_' in f])
            s += '\n'
        for k, v in sorted((self.__dict__.items()), key=(lambda x: x[0])):
            if is_primitives(v, inc_ndarray=False):
                s += '  %s: %s\n' % (ctext(k, 'cyan'), str(v))

        s = s[:-1] + '>'
        return s