# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/odin/ml/gmm_tmat.py
# Compiled at: 2019-08-13 03:51:05
# Size of source mod 2**32: 77007 bytes
""""
This module contains tools for Gaussian mixture modeling (GMM)
__author__ = 'Omid Sadjadi, Timothee Kheyrkhah'
__email__ = 'omid.sadjadi@nist.gov'
Modification and GPU-implementation by TrungNT
"""
import os, pickle, random, threading, time
from collections import Mapping, OrderedDict, defaultdict
import numpy as np, tensorflow as tf
from scipy import linalg
from six import string_types
from odin import backend as K
from odin.fuel import MmapArray
from odin.ml.base import BaseEstimator, DensityMixin, TransformerMixin
from odin.utils import MPI, Progbar, array_size, as_tuple, batching, cpu_count, ctext, defaultdictkey, eprint, is_number, segment_list, uuid, wprint
EPS = 1e-06
MINIMUM_GPU_BLOCK = 3840000

def zeroStat(post):
    """ Shape: (1, nmix)
  # sum over all samples
  # Zero-order statistics over all samples and dimension for
  each components
  """
    if K.is_tensor(post, inc_distribution=True, inc_variable=True):
        y = tf.reduce_sum(post, axis=0, keepdims=True, name='zero_stat')
    else:
        y = np.sum(post, axis=0, keepdims=True)
    return y


def firstStat(X, post):
    """ Shape: (feat_dim, nmix)
  First-order statistics over all samples for each components
  """
    if K.is_tensor(X, inc_distribution=True, inc_variable=True):
        y = tf.matmul((tf.transpose(X)), post, name='first_stat')
    else:
        y = np.dot(X.T, post)
    return y


def secondStat(X, post):
    """ Shape: (feat_dim, nmix)
  Second-order statistics over all samples for each components
  """
    if K.is_tensor(X, inc_distribution=True, inc_variable=True):
        y = tf.matmul((tf.transpose(tf.pow(X, 2))), post, name='second_stat')
    else:
        y = np.dot((X ** 2).T, post)
    return y


def logsumexp(X, axis):
    """
  Compute log(sum(exp(x),dim)) while avoiding numerical underflow
  """
    if K.is_tensor(X, inc_distribution=True, inc_variable=True):
        xmax = tf.reduce_max(X, axis=axis, keepdims=True)
        y = tf.add_n(inputs=[
         xmax,
         tf.log(tf.reduce_sum(input_tensor=(tf.exp(X - xmax)), axis=axis,
           keepdims=True))],
          name='llk')
    else:
        xmax = np.max(X, axis=axis, keepdims=True)
        y = xmax + np.log(np.sum(a=(np.exp(X - xmax)), axis=axis,
          keepdims=True))
    return y


def _split_jobs(n_samples, ncpu, device, gpu_factor):
    """ Return: jobs_cpu, jobs_gpu"""
    ngpu = get_ngpu()
    if ngpu == 0:
        device = 'cpu'
    if device == 'mix':
        njob = ncpu + 1 + ngpu * gpu_factor
    else:
        if device == 'cpu':
            njob = ncpu + 1
        else:
            if device == 'gpu':
                njob = ngpu + 1
            else:
                raise ValueError("Unknown device: '%s'" % device)
            jobs = np.linspace(start=0, stop=n_samples, num=njob,
              dtype='int32')
            jobs = list(zip(jobs, jobs[1:]))
            if device == 'mix':
                jobs_gpu = [(jobs[(i * gpu_factor)][0], jobs[(i * gpu_factor + gpu_factor - 1)][1]) for i in range(ngpu)]
                jobs_cpu = [jobs[i] for i in range(ngpu * gpu_factor, len(jobs))]
            else:
                if device == 'gpu':
                    jobs_gpu = jobs
                    jobs_cpu = []
                elif device == 'cpu':
                    jobs_gpu = []
                    jobs_cpu = jobs
    return (
     jobs_cpu, jobs_gpu)


def _create_batch(X, sad, start, end, batch_size, downsample, stochastic, seed, curr_nmix, curr_niter):
    """
  Return
  ------
  (X, n_selected_frame, n_original_frame)
  i.e. the number of select frames might be different from number
  of original frames after applying SAD
  """
    if stochastic:
        random.seed(seed + curr_nmix + curr_niter)
    else:
        random.seed(seed)
    all_batches = list(batching(n=(end - start), batch_size=batch_size))
    random.shuffle(all_batches)
    for batch_id, (batch_start, batch_end) in enumerate(all_batches):
        batch_start += start
        batch_end += start
        n_original_sample = batch_end - batch_start
        if batch_id == 0 or downsample == 1 or downsample > 1 and random.random() <= 1.0 / downsample:
            X_sad = X[batch_start:batch_end] if sad is None else X[batch_start:batch_end][sad[batch_start:batch_end].astype('bool')]
            yield (X_sad, X_sad.shape[0], n_original_sample)
        else:
            yield (
             None, n_original_sample, n_original_sample)


def _create_batch_indices(X, sad, indices, batch_size, downsample, stochastic, seed, curr_nmix, curr_niter):
    """
  Return
  ------
  (X, n_selected_frame, n_original_frame)
  i.e. the number of select frames might be different from number
  of original frames after applying SAD
  """
    if stochastic:
        random.seed(seed + curr_nmix + curr_niter)
    else:
        random.seed(seed)
    random.shuffle(indices)
    X_buffer = []
    n_original_buffer = 0
    n_selected_buffer = 0
    for batch_id, (name, (file_start, file_end)) in enumerate(indices):
        n_original_sample = file_end - file_start
        if batch_id == 0 or downsample == 1 or downsample > 1 and random.random() <= 1.0 / downsample:
            if n_original_sample <= batch_size:
                X_sad = X[file_start:file_end] if sad is None else X[file_start:file_end][sad[file_start:file_end].astype('bool')]
                X_buffer.append(X_sad)
                n_selected_buffer += X_sad.shape[0]
                n_original_buffer += n_original_sample
            else:
                for batch_start, batch_end in batching(n=n_original_sample, batch_size=batch_size):
                    batch_start = batch_start + file_start
                    batch_end = batch_end + file_start
                    X_sad = X[batch_start:batch_end] if sad is None else X[batch_start:batch_end][sad[batch_start:batch_end].astype('bool')]
                    if X_sad.shape[0] >= batch_size:
                        yield (
                         X_sad, X_sad.shape[0], n_original_sample)
                    else:
                        X_buffer.append(X_sad)
                        n_selected_buffer += X_sad.shape[0]
                        n_original_buffer += n_original_sample

        else:
            yield (
             None, n_original_sample, n_original_sample)
        if n_selected_buffer >= batch_size:
            yield (
             np.concatenate(X_buffer, axis=0), n_selected_buffer, n_original_buffer)
            X_buffer = []
            n_selected_buffer = 0
            n_original_buffer = 0

    if len(X_buffer) > 0:
        yield (
         np.concatenate(X_buffer, axis=0), n_selected_buffer, n_original_buffer)


class _ExpectationResults(object):
    __doc__ = ' ExpectationResult '

    def __init__(self, n_samples, nb_results, name, print_progress):
        super(_ExpectationResults, self).__init__()
        self.lock = threading.Lock()
        self.prog = Progbar(target=n_samples, print_report=True, print_summary=False,
          name=name)
        self.stats = [0.0 for i in range(int(nb_results))]
        self.print_progress = bool(print_progress)

    def update(self, res):
        """
    integer (or a number): number of processed samples (update the progress bar)
    otherwise: list of results (update the statistics)
    """
        self.lock.acquire()
        try:
            if is_number(res):
                if self.print_progress:
                    self.prog.add(res)
            else:
                for i, r in enumerate(res):
                    self.stats[i] += r

        finally:
            self.lock.release()


class GMM(DensityMixin, BaseEstimator, TransformerMixin):
    __doc__ = " Gaussian Mixture Model with diagonal covariance.\n\n  Parameters\n  ----------\n  nmix : int\n    number of mixtures\n  nmix_start : int\n    the algorithm start from given number of mixture, then perform\n    E-M and split to increase the mixtures to desire number\n  niter : int (default: 16)\n    number of iteration for E-M algorithm\n  dtype : {str, numpy.dtype} (default: float32)\n      desire dtype for mean, std, weights and input matrices\n      It is recommended to keep 'float32', since this speed up\n      a lot on GPU\n  allow_rollback : bool (default: True)\n      If True, reset the `mean`, `sigma` and `w` to the last\n      stable iteration, when `sigma` values smaller than 0\n  exit_on_error : bool (default: True)\n      Stop fitting when EM reach singular value and `sigma` become\n      numerical instabable (i.e. its values are smaller than 0)\n  batch_size : {int, 'auto'}\n      if 'auto', used `12 Megabytes` block for CPU batch and\n      `25 Megabytes` block for GPU batch\n  device : {'cpu', 'gpu', 'mix'}\n      'gpu' - run the computaiton on GPU\n      'cpu' - use multiprocessing for multiple cores\n      'mix' - use both GPU and multi-processing\n      * It is suggested to use mix of GPU and CPU if you have\n        more than 24 cores CPU, otherwise, 'gpu' gives the best\n        performance\n  ncpu : int\n      number of processes for parallel calculating Expectation\n  gpu_factor : int\n      how much jobs GPU will handle more than CPU\n      (i.e. `njob_gpu = gpu_factor * njob_cpu`)\n  stochastic_downsample : bool\n      if True, a subset of data is selected differently after\n      each iteration => the training is stochastic.\n      if False, a deterministic selection of data is performed\n      each iteration => the training is deterministic.\n  seed : int\n      random seed for reproducible\n  path : {str, None}\n      If given a path, save the model after everytime its\n      parameters changed (i.e. `maximization` or `gmm_mixup`\n      are called)\n  name : {str, None}\n      special name for this `Tmatrix` instance\n\n\n  Attributes\n  ----------\n  mu : (feat_dim, nmix)\n    mean vector for each component\n  sigma : (feat_dim, nmix)\n    standard deviation for each component\n  w : (1, nmix)\n    weights of each component\n\n  Note\n  ----\n  Memory throughput is the bottleneck in most of the case,\n  try to move the data to faster storage before fitting.\n\n  "
    STANDARD_CPU_BATCH_SIZE = 12582912
    STANDARD_GPU_BATCH_SIZE = 26214400

    def __init__(self, nmix, nmix_start=1, niter=16, dtype='float32', allow_rollback=True, exit_on_error=False, batch_size_cpu='auto', batch_size_gpu='auto', downsample=1, stochastic_downsample=True, device='cpu', ncpu=1, gpu_factor=80, seed=1234, path=None, name=None):
        super(GMM, self).__init__()
        self._path = path if isinstance(path, string_types) else None
        nmix = int(nmix)
        if nmix < 1:
            raise ValueError('Number of Mixture must be greater than 1.')
        else:
            self._nmix = nmix
            self._curr_nmix = np.clip(int(nmix_start), 1, self._nmix)
            self._feat_dim = None
            self._niter = int(niter)
            self.batch_size_cpu = batch_size_cpu
            self.batch_size_gpu = batch_size_gpu
            self.downsample = int(downsample)
            self.stochastic_downsample = bool(stochastic_downsample)
            self._seed = int(seed)
            self.gpu_factor = int(gpu_factor)
            if ncpu is None:
                ncpu = cpu_count() - 1
            self.ncpu = int(ncpu)
            self.set_device(device)
            self._llk_hist = defaultdict(list)
            self.allow_rollback = bool(allow_rollback)
            self.exit_on_error = bool(exit_on_error)
            self._stop_fitting = False
            self._dtype = np.dtype(dtype)
            if name is None:
                name = uuid(length=8)
                self._name = 'GMM_%s' % name
            else:
                self._name = str(name)

    def __getstate__(self):
        if not self.is_initialized:
            raise RuntimeError("GMM hasn't been initialized, nothing to save")
        return (
         self.mean, self.sigma, self.w,
         self.allow_rollback, self.exit_on_error,
         self._nmix, self._curr_nmix, self._feat_dim,
         self._niter, self.batch_size_cpu, self.batch_size_gpu,
         self.downsample, self.stochastic_downsample,
         self._seed, self._llk_hist,
         self.ncpu, self._device, self.gpu_factor,
         self._dtype, self._path, self._name)

    def __setstate__(self, states):
        self.mean, self.sigma, self.w, self.allow_rollback, self.exit_on_error, self._nmix, self._curr_nmix, self._feat_dim, self._niter, self.batch_size_cpu, self.batch_size_gpu, self.downsample, self.stochastic_downsample, self._seed, self._llk_hist, self.ncpu, self._device, self.gpu_factor, self._dtype, self._path, self._name = states
        self._stop_fitting = False
        self._feat_const = self.feat_dim * np.log(2 * np.pi)
        self.X_ = tf.placeholder(shape=(None, self.feat_dim), dtype=(self.dtype),
          name='GMM_input')
        self._resfresh_cpu_posterior()
        self._refresh_gpu_posterior()
        if self._device in ('gpu', 'mix'):
            if get_ngpu() == 0:
                wprint('Enabled GPU device, but no GPU found!')

    def __str__(self):
        if not self.is_initialized:
            return '<"%s" nmix:%d initialized:False>' % (self.name, self._nmix)
        else:
            s = '<"%s" nmix:%s ndim:%s mean:%s std:%s w:%s CPU:%s GPU:%s>' % (
             ctext(self.name, 'yellow'),
             ctext(self._nmix, 'cyan'),
             ctext(self._feat_dim, 'cyan'),
             ctext(self.mean.shape, 'cyan'),
             ctext(self.sigma.shape, 'cyan'),
             ctext(self.w.shape, 'cyan'),
             ctext(self.batch_size_cpu, 'cyan'),
             ctext(self.batch_size_gpu, 'cyan'))
            return s

    def set_device(self, device):
        device = str(device).lower()
        if device not in ('cpu', 'gpu', 'mix'):
            raise ValueError("`device` must be one of the following: 'cpu', 'gpu', or 'mix'")
        if device in ('gpu', 'mix'):
            if get_ngpu() == 0:
                wprint('Using GPU device but NO GPU detected, tensorflow will switch to slower CPU computation!')
        self._device = device
        return self

    @property
    def device(self):
        return self._device

    @property
    def path(self):
        return self._path

    @property
    def name(self):
        return self._name

    @property
    def is_initialized(self):
        return self._feat_dim is not None

    @property
    def is_fitted(self):
        return self._curr_nmix == self._nmix

    @property
    def nmix(self):
        return self._nmix

    @property
    def feat_dim(self):
        if not self.is_initialized:
            raise RuntimeError('GMM has not been initialized on data.')
        return self._feat_dim

    @property
    def history(self):
        """ Return the history of fitting this GMM in following format:
      `[(current_nmix, current_niter, llk), ...]`
    """
        return tuple(self._llk_hist)

    @property
    def dtype(self):
        return self._dtype

    def _resfresh_cpu_posterior(self):
        """ Refresh cached value for CPu computations. """
        expressions = {}
        precision = 1 / (self.sigma + EPS)
        C = np.sum((self.mean ** 2 * precision), axis=0, keepdims=True) + np.sum((np.log(self.sigma + EPS)), axis=0, keepdims=True) - 2 * np.log(self.w + EPS)
        mu_precision = self.mean * precision
        expressions['precision'] = precision
        expressions['mu_precision'] = mu_precision
        expressions['C'] = C
        self._GMM__expressions_cpu = expressions

    def _refresh_gpu_posterior(self):
        """ Call this function when you update the mixture
    components.

    Unlike CPU computation, tensorflow graph on need to
    renew it placeholder which represent: mu, sigma, weight
    when GMM mixup.
    """
        expressions = {}
        if self._curr_nmix < self.nmix:
            scope = self.name + str(self._curr_nmix)
        else:
            scope = self.name
        with tf.variable_scope(scope):
            mu = tf.placeholder(shape=(self.feat_dim, self._curr_nmix), dtype=(self.dtype),
              name='GMM_mu')
            sigma = tf.placeholder(shape=(self.feat_dim, self._curr_nmix), dtype=(self.dtype),
              name='GMM_sigma')
            w = tf.placeholder(shape=(1, self._curr_nmix), dtype=(self.dtype),
              name='GMM_weight')
            expressions['mu'] = mu
            expressions['sigma'] = sigma
            expressions['w'] = w
            precision = 1 / (sigma + EPS)
            C = tf.reduce_sum((mu ** 2 * precision), axis=0, keepdims=True) + tf.reduce_sum((tf.log(sigma + EPS)), axis=0, keepdims=True) - 2 * tf.log(w)
            D = tf.matmul(self.X_ ** 2, precision) - 2 * tf.matmul(self.X_, mu * precision) + self.feat_dim * np.log(2 * np.pi)
            logprob = tf.multiply(x=tf.constant((-0.5), dtype=(self.dtype)), y=(C + D),
              name='logprob')
            expressions['logprob'] = logprob
            llk = logsumexp(logprob, axis=1)
            post = tf.exp((logprob - llk), name='postprob')
            expressions['llk'] = llk
            expressions['post'] = post
            expressions['zero'] = zeroStat(post)
            expressions['first'] = firstStat(self.X_, post)
            expressions['second'] = secondStat(self.X_, post)
            expressions['L'] = tf.reduce_sum(llk, axis=None, name='sum_llk')
        self._GMM__expressions_gpu = expressions

    def initialize(self, X):
        indices = None
        if isinstance(X, (tuple, list)):
            tmp = [i for i in X if hasattr(i, 'shape')][0]
            indices = [i for i in X if i != tmp][0]
            X = tmp
        if not isinstance(X, np.ndarray):
            raise ValueError('`X` must be numpy.ndarray')
        else:
            if isinstance(indices, Mapping):
                indices = list(indices.items())
            else:
                if not isinstance(indices, (tuple, list, np.ndarray, type(None))):
                    raise ValueError('`indices` must be None, Mapping, tuple, list or numpy.ndarray')
                else:
                    if hasattr(X, 'ndim'):
                        ndim = X.ndim
                    else:
                        if hasattr(X, 'get_shape'):
                            ndim = len(X.shape.as_list())
                        else:
                            raise ValueError('Cannot number of dimension from input.')
                if hasattr(X, 'shape'):
                    feat_dim = X.shape[1]
                else:
                    if hasattr(X, 'get_shape'):
                        feat_dim = X.shape.as_list()[1]
                    else:
                        raise ValueError('Cannot get feature dimension from input.')
        if self.is_initialized:
            if ndim != 2 or feat_dim != self._feat_dim:
                raise RuntimeError('Input must be 2-D matrix with the 1st dimension equal to: %d' % feat_dim)
            return (X, indices)
        else:
            self._feat_dim = int(feat_dim)
            self._feat_const = self.feat_dim * np.log(2 * np.pi)
            if isinstance(self.batch_size_cpu, string_types):
                self.batch_size_cpu = int(GMM.STANDARD_CPU_BATCH_SIZE / (self.feat_dim * self.dtype.itemsize))
            if isinstance(self.batch_size_gpu, string_types):
                self.batch_size_gpu = int(GMM.STANDARD_GPU_BATCH_SIZE / (self.feat_dim * self.dtype.itemsize))
            self.X_ = tf.placeholder(shape=(None, self.feat_dim), dtype=(self.dtype),
              name='GMM_input')
            self.mean = np.zeros((feat_dim, self._curr_nmix), dtype=(self._dtype))
            self.sigma = np.ones((feat_dim, self._curr_nmix), dtype=(self._dtype))
            self.w = np.ones((1, self._curr_nmix), dtype=(self._dtype))
            self._resfresh_cpu_posterior()
            self._refresh_gpu_posterior()
            return (X, indices)

    def fit(self, X, y=None):
        """
    Parameters
    ----------
    X : {numpy.ndarray, tuple, list}
      in case a tuple is given, two options are considered:
       - length of the list is 1: only training feature is given
       - length of the list is 2: training data (numpy.ndarray),
       indices or sad indices (numpy.ndarray)
       - length of the list is 3: training data (numpy.ndarray),
       sad indices (numpy.ndarray), indices
      where the `indices` is a dictionary of the mapping
      'file_name' -> (start_index, end_index) in the training
      data array

    NOTE
    ----
    from 1, 2, 4 components, python multi-threading is fastest
    from 8, 16 components, python multi-processing is fastest
    from > 32 components, GPU scales much much better.
    """
        if not isinstance(X, (tuple, list)):
            X = (
             X,)
        else:
            sad = None
            indices = None
            if len(X) == 1:
                data = X[0]
            else:
                if len(X) == 2:
                    if hasattr(X[1], 'shape'):
                        if X[0].shape[0] == X[1].shape[0]:
                            data, sad = X
                    data, indices = X
                else:
                    if len(X) == 3:
                        data, sad, indices = X
                    else:
                        raise ValueError('No support for `X` in type of list with length: %d' % len(X))
            assert hasattr(data, 'shape') and data.ndim == 2, 'Input data must be instance of 2-D ndarray but give: %s' % str(type(data))
            if indices is not None:
                if isinstance(indices, Mapping):
                    indices = list(indices.items())
                indices = sorted(indices, key=(lambda x: x[1][0]))
                X = (data, indices)
            else:
                X = data
        niter = [1, 2, 4, 4, 4, 4, 6, 6, 10, 10, 10, 10, 10, 16, 16]
        niter[int(np.log2(self._nmix))] = self._niter
        self._stop_fitting = False
        while 1:
            curr_nmix = self._curr_nmix
            last_niter = len(self._llk_hist[curr_nmix])
            idx = int(np.log2(curr_nmix))
            curr_niter = niter[idx] - last_niter
            if curr_niter > 0:
                for i in range(curr_niter):
                    self.expectation_maximization(X, sad=sad, print_progress=True)
                    if self._stop_fitting:
                        return self

                print('---')
            if curr_nmix < self._nmix:
                self.gmm_mixup()
            else:
                break

        return self

    def score(self, X, y=None):
        """ Compute the log-likelihood of each example to
    the Mixture of Components.
    """
        post = self.logprob(X)
        return logsumexp(post, axis=1)

    def transform(self, X, zero=True, first=True, device=None):
        """ Compute centered statistics given X and fitted mixtures

    Parameters
    ----------
    X : ndarray
      input feature [n_samples, feat_dim] (e.g. all frames
      of an utterance for audio data)
    zero : bool (default: True)
      if True, return the zero-th order statistics
    first : bool (default: True)
      if True, return the first order statistics
    device : {None, 'cpu', 'gpu'}
      select device for execute the expectation calculation

    Return
    ------
    zero-th statistics: [1, nmix]
      e.g. the assignment score each samples to each components, hence,
      `#frames = Z.sum()`
    first statistics: [1, feat_dim * nmix]
      dot-product of each sample and the posteriors.

    NOTE
    ----
    For more option check `GMM.expectation`
    """
        if device is None:
            device = self._device
        else:
            zero = bool(zero)
            first = bool(first)
            if not zero:
                if not first:
                    raise ValueError('One of `zero` or `first` must be True')
            assert X.ndim == 2 and X.shape[1] == self.feat_dim, '`X` must be 2-D matrix, with `X.shape[1]=%d`; but given: %s' % (
             self.feat_dim, str(X.shape))
            Z = None
            F = None
            F_hat = None
            results = self._fast_expectation(X, zero=zero, first=first, second=False,
              llk=False,
              on_gpu=(device != 'cpu'))
            if zero:
                if first:
                    Z, F = results
                    F_hat = np.reshape((F - self.mean * Z), newshape=(
                     1, self.feat_dim * self._curr_nmix),
                      order='F')
                    return (
                     Z, F_hat)
            if zero:
                if not first:
                    Z = results
                    return Z
            if not zero and first:
                F = results
                F_hat = np.reshape((F - self.mean * Z), newshape=(
                 1, self.feat_dim * self._curr_nmix),
                  order='F')
                return F_hat

    def transform_to_disk(self, X, indices, sad=None, pathZ=None, pathF=None, name_path=None, dtype='float32', device='cpu', ncpu=None, override=True):
        """ Same as `transform`, however, save the transformed statistics
    to file using `odin.fuel.MmapArray`

    Return
    ------
    zero-th statistics: [1, nmix]
      e.g. the assignment score each samples to each components, hence,
      `#frames = Z.sum()`
    first statistics: [1, feat_dim * nmix]
      dot-product of each sample and the posteriors.

    Note
    ----
    If your data contain many very long utterances, it is suggested to use
    `device='gpu'`, otherwise, 'cpu' is mostly significant faster.
    """
        if isinstance(indices, Mapping):
            indices = sorted((indices.items()), key=(lambda x: x[1][0]))
        else:
            if sad is not None:
                if not sad.shape[0] == X.shape[0]:
                    raise AssertionError('Number of samples in `X` (%d) and `sad` (%d) are mismatched' % (len(X), len(sad)))
                else:
                    if not sad.ndim == 1:
                        assert sad.ndim == 2 and sad.shape[1] == 1, 'Invalid shape for `sad.shape=%s`' % str(sad.shape)
                    else:
                        if device is None:
                            device = self._device
                        on_gpu = True if (device != 'cpu' and get_ngpu() > 0) else False
                        name_list = []
                        prog = Progbar(target=(len(indices)), print_report=True,
                          print_summary=True,
                          name='Saving zero-th and first order statistics')
                        if pathZ is not None:
                            if os.path.exists(pathZ):
                                if override:
                                    os.remove(pathZ)
                            z_dat = MmapArray(path=pathZ, dtype=dtype, shape=(
                             None, self.nmix))
                        else:
                            z_dat = None
                    if pathF is not None:
                        if os.path.exists(pathF):
                            if override:
                                os.remove(pathF)
                        f_dat = MmapArray(path=pathF, dtype=dtype, shape=(
                         None, self.nmix * self.feat_dim))
                    else:
                        f_dat = None

                def _update_zf(Z, F):
                    if z_dat is not None:
                        z_dat.append(Z)
                    if f_dat is not None:
                        f_dat.append(F)

                def _batched_transform(s, e, on_gpu):
                    reduction = np.floor(np.power(2, self._curr_nmix / 1024))
                    batch_size = self.batch_size_gpu if on_gpu else self.batch_size_cpu
                    batch_size = int(batch_size / reduction)
                    x = X[s:e]
                    if sad is not None:
                        x = x[sad[s:e].astype('bool')]
                    else:
                        if x.shape[0] <= batch_size:
                            res = [
                             self._fast_expectation(x, zero=(z_dat is not None or f_dat is not None),
                               first=(f_dat is not None),
                               second=False,
                               llk=False,
                               on_gpu=on_gpu)]
                        else:
                            res = [self._fast_expectation((x[start:end]), zero=(z_dat is not None or f_dat is not None), first=(f_dat is not None), second=False, llk=False, on_gpu=on_gpu) for start, end in batching(n=(x.shape[0]), batch_size=batch_size)]
                        Z = sum(r[0] for r in res)
                        if len(res[0]) == 2:
                            F = sum(r[1] for r in res)
                            F = np.reshape(a=(F - self.mean * Z), newshape=(
                             Z.shape[0], self._feat_dim * self._curr_nmix),
                              order='F')
                        else:
                            F = None
                    return (
                     Z, F)

                if on_gpu:
                    for n, (start, end) in indices:
                        Z, F = _batched_transform(start, end, on_gpu=True)
                        _update_zf(Z, F)
                        name_list.append(n)
                        prog.add(1)

                else:

                    def map_func(j):
                        Z_list, F_list = [], []
                        name = []
                        for n, (start, end) in j:
                            name.append(n)
                            Z, F = _batched_transform(start, end, on_gpu=False)
                            if z_dat is not None:
                                Z_list.append(Z)
                            if f_dat is not None:
                                F_list.append(F)
                            yield 1

                        if len(Z_list) > 0:
                            Z_list = np.concatenate(Z_list, axis=0)
                        if len(F_list) > 0:
                            F_list = np.concatenate(F_list, axis=0)
                        yield (
                         name, Z_list, F_list)

                    mpi = MPI(jobs=(list(indices.items()) if isinstance(indices, Mapping) else indices),
                      func=map_func,
                      ncpu=(self.ncpu if ncpu is None else int(ncpu)),
                      batch=(max(2, self.batch_size_cpu // (self.ncpu * 2))),
                      hwm=33554432)
                    for results in mpi:
                        if is_number(results):
                            prog['Z_path'] = str(pathZ)
                            prog['F_path'] = str(pathF)
                            prog.add(results)
                        else:
                            name, Z, F = results
                            _update_zf(Z, F)
                            name_list += name

            else:
                if z_dat is not None:
                    z_dat.flush()
                    z_dat.close()
                if f_dat is not None:
                    f_dat.flush()
                    f_dat.close()
            if isinstance(name_path, string_types):
                np.savetxt(fname=name_path, X=name_list, fmt='%s')
        return name_list

    def logprob(self, X):
        """ Shape: [batch_size, nmix]
    the log probability of each observations to each components
    given the GMM.
    """
        self.initialize(X)
        if self._device != 'cpu':
            feed_dict = {self.X_: X}
            feed_dict[self._GMM__expressions_gpu['mu']] = self.mean
            feed_dict[self._GMM__expressions_gpu['sigma']] = self.sigma
            feed_dict[self._GMM__expressions_gpu['w']] = self.w
            return K.eval(x=(self._GMM__expressions_gpu['logprob']), feed_dict=feed_dict)
        else:
            precision = self._GMM__expressions_cpu['precision']
            mu_precision = self._GMM__expressions_cpu['mu_precision']
            C = self._GMM__expressions_cpu['C']
            X_2 = X ** 2
            D = np.dot(X_2, precision) - 2 * np.dot(X, mu_precision) + self._feat_const
            logprob = -0.5 * (C + D)
            return logprob

    def postprob(self, X, gpu='auto'):
        """ Shape: (batch_size, nmix)
    The posterior probability of mixtures for each frame
    """
        self.initialize(X)
        if self._device != 'cpu':
            feed_dict = {self.X_: X}
            feed_dict[self._GMM__expressions_gpu['mu']] = self.mean
            feed_dict[self._GMM__expressions_gpu['sigma']] = self.sigma
            feed_dict[self._GMM__expressions_gpu['w']] = self.w
            return K.eval(x=(self._GMM__expressions_gpu['post']), feed_dict=feed_dict)
        else:
            precision = self._GMM__expressions_cpu['precision']
            mu_precision = self._GMM__expressions_cpu['mu_precision']
            C = self._GMM__expressions_cpu['C']
            X_2 = X ** 2
            D = np.dot(X_2, precision) - 2 * np.dot(X, mu_precision) + self._feat_const
            logprob = -0.5 * (C + D)
            llk = logsumexp(logprob, axis=1)
            post = np.exp(logprob - llk)
            return post

    def llk(self, X, gpu='auto'):
        """ Shape: (batch_size, 1)
    The log-likelihood value of each frame to all components
    """
        self.initialize(X)
        if self._device != 'cpu':
            feed_dict = {self.X_: X}
            feed_dict[self._GMM__expressions_gpu['mu']] = self.mean
            feed_dict[self._GMM__expressions_gpu['sigma']] = self.sigma
            feed_dict[self._GMM__expressions_gpu['w']] = self.w
            return K.eval(x=(self._GMM__expressions_gpu['llk']), feed_dict=feed_dict)
        else:
            precision = self._GMM__expressions_cpu['precision']
            mu_precision = self._GMM__expressions_cpu['mu_precision']
            C = self._GMM__expressions_cpu['C']
            X_2 = X ** 2
            D = np.dot(X_2, precision) - 2 * np.dot(X, mu_precision) + self._feat_const
            logprob = -0.5 * (C + D)
            llk = logsumexp(logprob, axis=1)
            return llk

    def _fast_expectation(self, X, zero=True, first=True, second=True, llk=True, on_gpu=False):
        if on_gpu:
            Z, F, S, L = [self._GMM__expressions_gpu[name] for name in ('zero', 'first',
                                                                        'second',
                                                                        'L')]
            feed_dict = {self.X_: X}
            feed_dict[self._GMM__expressions_gpu['mu']] = self.mean
            feed_dict[self._GMM__expressions_gpu['sigma']] = self.sigma
            feed_dict[self._GMM__expressions_gpu['w']] = self.w
            outputs = [i for i, j in zip((Z, F, S, L), (
             zero, first, second, llk)) if j]
            results = K.eval(x=outputs, feed_dict=feed_dict)
        else:
            results = []
            precision = self._GMM__expressions_cpu['precision']
            mu_precision = self._GMM__expressions_cpu['mu_precision']
            C = self._GMM__expressions_cpu['C']
            X_2 = X ** 2
            D = np.dot(X_2, precision) - 2 * np.dot(X, mu_precision) + self._feat_const
            logprob = -0.5 * (C + D)
            LLK = logsumexp(logprob, axis=1)
            post = np.exp(logprob - LLK)
            if zero:
                Z = zeroStat(post)
                results.append(Z)
            if first:
                F = firstStat(X, post)
                results.append(F)
            if second:
                S = np.dot(X_2.T, post)
                results.append(S)
        if llk:
            L = np.sum(LLK, axis=None)
            results.append(L)
        if len(results) > 1:
            return results
        else:
            return results[0]

    def expectation(self, X, sad=None, zero=True, first=True, second=True, llk=True, device=None, print_progress=True):
        """
    Parameters
    ----------
    X : numpy.ndarray [batch_size, feat_dim]
        input array, with feature dimension is the final dimension
    zero : bool (default: True)
        if True, return zero-order statistics
    first : bool (default: True)
        if True, return first-order statistics
    second : bool (default: True)
        if True, return second-order statistics
    llk : bool (default: True)
        if True, return the mean log-likelihood
    device : {None, 'cpu', 'gpu', 'mix'}
        None - keep the orginal device specified in init
        'gpu' - run the computaiton on GPU
        'cpu' - use multiprocessing for multiple cores
        'mix' - use both GPU and multi-processing
    print_progress : bool (default: True)
        if fitting required multiple batches, print the
        progress bar.

    Return
    ------
    The order of return value:
    zero  (optional) : ndarray [1, nmix]
    first (optional) : ndarray [feat_dim, nmix]
    second(optional) : ndarray [feat_dim, nmix]
    llk   (optional) : scalar ()
    """
        X, indices = self.initialize(X)
        if sad is not None:
            assert sad.shape[0] == X.shape[0], 'Number of samples for X and sad mismatch X.shape=%s and sad.shape=%s' % (
             X.shape, sad.shape)
        else:
            if not sad.ndim == 1:
                assert sad.ndim == 2 and sad.shape[1] == 1, '`sad` must be 1-D array or 2-D array with second dimension equal to 1'
            if indices is None:
                n_samples = X.shape[0]
            else:
                n_samples = sum(end - start for name, (start, end) in indices)
        device = self._device if device is None else str(device).lower()
        if device not in ('gpu', 'cpu', 'mix'):
            raise ValueError("`device` can only be of the following:'gpu', 'cpu', and 'mix'.")
        if n_samples <= self.batch_size_cpu and self._device == 'cpu' or n_samples <= self.batch_size_gpu and self._device in ('gpu',
                                                                                                                               'mix'):
            if indices is None:
                X_sad = X if sad is None else X[sad.astype('bool')]
            else:
                X_sad = []
                for name, (start, end) in indices:
                    X_sad.append(X[start:end] if sad is None else X[start:end][sad[start:end].astype('bool')])

                X_sad = np.concatenate(X_sad, axis=0)
            results = self._fast_expectation(X_sad, zero, first, second, llk, on_gpu=(self._device != 'cpu'))
            if llk:
                if isinstance(results, (tuple, list)):
                    results = tuple(results[:-1]) + (np.array(results[(-1)] / X_sad.shape[0]),)
                else:
                    results = np.array(results / X_sad.shape[0])
            return results
        else:
            curr_niter = len(self._llk_hist[self._curr_nmix])
            curr_nmix = self._curr_nmix

            def map_expectation(start_end_gpu):
                reduction = np.floor(np.power(2, curr_nmix / 1024))
                get_batch_size = lambda on_gpu: int((self.batch_size_gpu if on_gpu else self.batch_size_cpu) / reduction)
                if indices is None:
                    (start, end), on_gpu = start_end_gpu
                    batch_iterator = _create_batch(X, sad, start, end, batch_size=(get_batch_size(on_gpu)),
                      downsample=(self.downsample),
                      stochastic=(self.stochastic_downsample),
                      seed=(self._seed),
                      curr_nmix=curr_nmix,
                      curr_niter=curr_niter)
                else:
                    jobs, on_gpu = start_end_gpu
                    batch_iterator = _create_batch_indices(X, sad, jobs, batch_size=(get_batch_size(on_gpu)),
                      downsample=(self.downsample),
                      stochastic=(self.stochastic_downsample),
                      seed=(self._seed),
                      curr_nmix=curr_nmix,
                      curr_niter=curr_niter)
                results = [0.0, 0.0, 0.0, 0.0, 0]
                for y, n_selected_frame, n_original_sample in batch_iterator:
                    if y is not None:
                        for i, res in enumerate(self._fast_expectation(y, zero=True, first=True, second=True, llk=True,
                          on_gpu=on_gpu)):
                            results[i] += res

                        results[(-1)] += n_selected_frame
                    yield n_original_sample

                yield tuple(results)

            def thread_expectation(results, start_end):
                for res in map_expectation((start_end, True)):
                    results.update(res)

            jobs_cpu, jobs_gpu = _split_jobs(n_samples=n_samples, ncpu=(self.ncpu),
              device=device,
              gpu_factor=(self.gpu_factor))
            if indices is not None:
                indices = list(indices)
                new_gpu_jobs = []
                for s, e in jobs_gpu:
                    j = []
                    n = e - s
                    while n > 0 and len(indices) >= 1:
                        tmp = indices.pop()
                        n -= tmp[1][1] - tmp[1][0]
                        j.append(tmp)

                    new_gpu_jobs.append(j)

                jobs_gpu = new_gpu_jobs
                new_cpu_jobs = []
                for s, e in jobs_cpu:
                    j = []
                    n = e - s
                    while n > 0 and len(indices) >= 1:
                        tmp = indices.pop()
                        n -= tmp[1][1] - tmp[1][0]
                        j.append(tmp)

                    new_cpu_jobs.append(j)

                jobs_cpu = new_cpu_jobs
            results = _ExpectationResults(n_samples=n_samples, nb_results=5, name=('[GMM] cmix:%d nmix:%d ndim:%d iter:%d' % (
             curr_nmix, self.nmix, self.feat_dim, curr_niter + 1)),
              print_progress=print_progress)
            mpi = []
            if len(jobs_cpu) > 0:
                mpi = MPI(jobs=[(j, False) for j in jobs_cpu], func=map_expectation,
                  ncpu=(self.ncpu),
                  batch=1,
                  hwm=33554432,
                  backend='python')
            gpu_threads = [threading.Thread(target=thread_expectation, args=(results, j)) for j in jobs_gpu]
            for t in gpu_threads:
                t.start()

            for res in mpi:
                results.update(res)

            for t in gpu_threads:
                t.join()

            Z, F, S, L, nfr = results.stats
            L = L / nfr if nfr > 0 else 0
            results = []
            if zero:
                results.append(Z)
            if first:
                results.append(F)
            if second:
                results.append(S)
            if llk:
                results.append(L)
            if len(results) == 1:
                return results[0]
            return results

    def maximization(self, Z, F, S, floor_const=None):
        """
    Parameters
    ----------
    Z : numpy.ndarray (1, nmix)
        zero statistics
    F : numpy.ndarray (feat_dim, nmix)
        first-order statistics
    S : numpy.ndarray (feat_dim, nmix)
        second-order statistics
    floor_const : {None, small float}
        numerical stablize the sigma (e.g. 1e-3)
    """
        last_parameters = [
         np.array(self.w),
         np.array(self.mean),
         np.array(self.sigma)]
        iN = 1.0 / (Z + EPS)
        self.w = Z / Z.sum()
        self.mean = F * iN
        self.sigma = S * iN - self.mean ** 2
        if floor_const is not None:
            vFloor = self.sigma.dot(self.w.T) * floor_const
            self.sigma = self.sigma.clip(vFloor)
        if np.any(self.sigma == 0.0):
            wprint('[GMM] Some Sigma elements go to zeros')
        if np.any(self.sigma < 0.0):
            eprint('[GMM] Numberical instability, Sigma values went smaller than 0!')
            if self.allow_rollback:
                self.w = last_parameters[0]
                self.mean = last_parameters[1]
                self.sigma = last_parameters[2]
            else:
                self.sigma = np.clip((self.sigma), a_min=0.0, a_max=(np.Inf))
            if self.exit_on_error:
                self._stop_fitting = True
        self._resfresh_cpu_posterior()
        del last_parameters
        return self

    def expectation_maximization(self, X, sad=None, device=None, print_progress=True):
        self.initialize(X)
        curr_nmix = self._curr_nmix
        curr_niter = len(self._llk_hist[curr_nmix]) + 1
        start_time = time.time()
        Z, F, S, L = self.expectation(X, sad=sad, device=device,
          print_progress=print_progress)
        time_Estep = time.time() - start_time
        start_time = time.time()
        self.maximization(Z, F, S)
        time_Mstep = time.time() - start_time
        self._llk_hist[self._curr_nmix].append(L)
        if print_progress:
            print('#mix:%s #iter:%s llk:%s Estep:%s(s) Mstep:%s(s)' % (
             ctext('%.2d' % curr_nmix, 'cyan'),
             ctext('%.2d' % curr_niter, 'yellow'),
             ctext('%.4f' % L, 'yellow'),
             ctext('%.2f' % time_Estep, 'yellow'),
             ctext('%.4f' % time_Mstep, 'yellow')))
        if self.path is not None:
            with open(self.path, 'wb') as (f):
                pickle.dump(self, f)
        return self

    def gmm_mixup(self):
        if self._curr_nmix >= self._nmix:
            return
        else:
            ndim, nmix = self.sigma.shape
            sig_max, arg_max = self.sigma.max(0), self.sigma.argmax(0)
            eps = np.zeros((ndim, nmix), dtype='f')
            eps[(arg_max, np.arange(nmix))] = np.sqrt(sig_max)
            perturb = 0.55 * eps
            if self._curr_nmix * 2 <= self._nmix:
                self.mean = np.c_[(self.mean - perturb, self.mean + perturb)]
                self.sigma = np.c_[(self.sigma, self.sigma)]
                self.w = 0.5 * np.c_[(self.w, self.w)]
            else:
                self.mean = np.c_[(self.mean - perturb, self.mean + perturb)][:, :self.nmix]
                self.sigma = np.c_[(self.sigma, self.sigma)]
                self.sigma = self.sigma[:, :self.nmix]
                self.w = 0.5 * np.c_[(self.w, self.w)]
                self.w = self.w[:, :self.nmix]
            self._curr_nmix = min(2 * self._curr_nmix, self.nmix)
            self._refresh_gpu_posterior()
            self._resfresh_cpu_posterior()
            if self.path is not None:
                with open(self.path, 'wb') as (f):
                    pickle.dump(self, f)
            return self


class Tmatrix(DensityMixin, BaseEstimator, TransformerMixin):
    __doc__ = " Tmatrix training for i-vectors extraction\n  based on total varibility space.\n\n  Parameters\n  ----------\n  tv_dim : int\n    dimension of T-matrix\n  gmm : odin.ml.gmm.GMM\n    initialized and fitted GMM\n  niter : int (default: 16)\n    number of iteration for E-M algorithm\n  batch_size : {int, 'auto'}\n      if 'auto', used `25 Megabytes` block for batch size.\n  dtype : {str, numpy.dtype} (default: float64)\n      desire dtype for mean, std, weights and input matrices\n      The computation of Tmatrix involves matrices invert, it\n      is recommended to keep 'float64' since significant\n      amount of computation can be performed on CPU.\n  device : {'cpu', 'gpu', 'mix'}\n      'gpu' - run the computaiton on GPU\n      'cpu' - use multiprocessing for multiple cores\n      'mix' - use both GPU and multi-processing\n      * It is suggested to use mix of GPU and CPU if you have\n        more than 24 cores CPU, otherwise, 'gpu' gives the best\n        performance\n  ncpu : int (default: 1)\n      number of processes for parallel calculating Expectation\n      NOTE: it is recommended to keep number of CPU to 1\n      since the numpy implementation of matrix invert using\n      multi-thread already.\n  gpu_factor : int\n      how much jobs GPU will handle more than CPU\n      (i.e. `njob_gpu = gpu_factor * njob_cpu`)\n  cache_path : str\n    path to cache folder when fitting\n  seed : int\n      random seed for reproducible\n  path : {str, None}\n      If given a path, save the model after everytime its\n      parameters changed (i.e. `maximization` is called)\n  name : {str, None}\n      special name for this `Tmatrix` instance\n\n  Attributes\n  ----------\n  Tm : (tv_dim, feat_dim * nmix)\n    latent vector for each mixtures and features\n  T_invS : (tv_dim, feat_dim * nmix)\n    Tm / GMM.Sigma\n  T_invS_Tt : (nmix, tv_dim * (tv_dim + 1) / 2)\n    lower half of the inverted T-matrix\n\n  Note\n  ----\n  If you have built numpy with an optimized BLAS like OpenBLAS or\n  MKL (which is the case if you got numpy from pypi or anaconda),\n  it's likely that the inv operation which is probably the bottleneck\n  of your code is already multithreaded.\n  Therefore there is no point trying to parallelize on top of that.\n\n  You should increase the `batch_size` instead of `ncpu` if there\n  are idle resources.\n\n  "
    STANDARD_CPU_BATCH_SIZE = 67108864
    STANDARD_GPU_BATCH_SIZE = 67108864

    def __init__(self, tv_dim, gmm, niter=16, dtype='float64', batch_size_cpu='auto', batch_size_gpu='auto', device='mix', ncpu=1, gpu_factor=3, cache_path='/tmp', seed=1234, path=None, name=None):
        super(Tmatrix, self).__init__()
        if not (isinstance(gmm, GMM) and gmm.is_initialized and gmm.is_fitted):
            raise ValueError('`gmm` must be instance of odin.ml.gmm.GMM both is_initialized and is_fitted.')
        else:
            self._is_fitted = False
            self.niter = niter
            self._tv_dim = tv_dim
            self._t2_dim = tv_dim * (tv_dim + 1) // 2
            self._feat_dim = gmm.feat_dim
            self._nmix = gmm.nmix
            self._gmm = gmm
            self._path = path if isinstance(path, string_types) else None
            self._seed = seed
            self._llk_hist = []
            if name is None:
                name = uuid(length=8)
                self._name = 'Tmatrix_%s' % name
            else:
                self._name = str(name)
        if not os.path.isdir(cache_path):
            raise ValueError('`cache_path` must be a directory.')
        self.cache_path = cache_path
        self._dtype = np.dtype(dtype)
        if isinstance(batch_size_cpu, string_types):
            batch_size_cpu = int(Tmatrix.STANDARD_CPU_BATCH_SIZE / (self.feat_dim * self.nmix * self.dtype.itemsize + self.nmix * self.dtype.itemsize))
        self.batch_size_cpu = batch_size_cpu
        if isinstance(batch_size_gpu, string_types):
            batch_size_gpu = int(Tmatrix.STANDARD_GPU_BATCH_SIZE / (self.feat_dim * self.nmix * self.dtype.itemsize + self.nmix * self.dtype.itemsize))
        self.batch_size_gpu = batch_size_gpu
        self.set_device(device)
        if ncpu is None:
            ncpu = cpu_count() // 2
        self.ncpu = int(ncpu)
        self.gpu_factor = int(gpu_factor)
        self.Im = np.eye((self.tv_dim), dtype=(self.dtype))
        self.Sigma = np.array(gmm.sigma.reshape((1, self.feat_dim * self.nmix), order='F'),
          dtype=(self.dtype))
        np.random.seed(self._seed)
        self.Tm = (np.random.randn(self.tv_dim, self.feat_dim * self.nmix) * self.Sigma.sum() * 0.001).astype(self.dtype)
        self.T_invS_Tt = np.empty((self.nmix, self.t2_dim), dtype=(self.dtype))
        self._itril = np.tril_indices(self.tv_dim)
        self._Ex_Exx_llk = defaultdictkey(lambda nfiles: (
         np.empty((nfiles, self.tv_dim), dtype=(self.dtype)),
         np.empty((nfiles, self.t2_dim), dtype=(self.dtype)),
         np.empty((nfiles, 1), dtype=(self.dtype))))
        self._refresh_T_statistics()
        self._refresh_gpu()

    def __getstate__(self):
        return (
         self.Im, self.Sigma, self.Tm, self._gmm,
         self._tv_dim, self._t2_dim, self._feat_dim, self._nmix,
         self._seed, self._llk_hist,
         self.batch_size_cpu, self.batch_size_gpu,
         self.niter, self.ncpu, self._device, self.gpu_factor,
         self.cache_path, self._dtype,
         self._is_fitted, self._path, self._name)

    def __setstate__(self, states):
        self.Im, self.Sigma, self.Tm, self._gmm, self._tv_dim, self._t2_dim, self._feat_dim, self._nmix, self._seed, self._llk_hist, self.batch_size_cpu, self.batch_size_gpu, self.niter, self.ncpu, self._device, self.gpu_factor, self.cache_path, self._dtype, self._is_fitted, self._path, self._name = states
        self.T_invS_Tt = np.empty((self.nmix, self.t2_dim), dtype=(self.dtype))
        self._itril = np.tril_indices(self.tv_dim)
        self._Ex_Exx_llk = defaultdictkey(lambda nfiles: (
         np.empty((nfiles, self.tv_dim), dtype=(self.dtype)),
         np.empty((nfiles, self.t2_dim), dtype=(self.dtype)),
         np.empty((nfiles, 1), dtype=(self.dtype))))
        self._refresh_T_statistics()
        self._refresh_gpu()
        if self._device in ('gpu', 'mix'):
            if get_ngpu() == 0:
                wprint('Enabled GPU device, but no GPU found!')

    def __str__(self):
        s = '<"%s" Tdim:%s nmix:%s ndim:%s niter:%s CPU:%s GPU:%s>' % (
         ctext(self.name, 'yellow'),
         ctext(self._tv_dim, 'cyan'),
         ctext(self._nmix, 'cyan'),
         ctext(self._feat_dim, 'cyan'),
         ctext(len(self._llk_hist), 'cyan'),
         ctext(self.batch_size_cpu, 'cyan'),
         ctext(self.batch_size_gpu, 'cyan'))
        return s

    def set_device(self, device):
        device = str(device).lower()
        if device not in ('cpu', 'gpu', 'mix'):
            raise ValueError("`device` must be one of the following: 'cpu', 'gpu', or 'mix'")
        if device in ('gpu', 'mix'):
            if get_ngpu() == 0:
                wprint('Using GPU device but NO GPU detected, tensorflow will switch to slower CPU computation!')
        self._device = device
        return self

    @property
    def device(self):
        return self._device

    @property
    def feat_dim(self):
        return self._feat_dim

    @property
    def tv_dim(self):
        return self._tv_dim

    @property
    def t2_dim(self):
        return self._t2_dim

    @property
    def nmix(self):
        return self._nmix

    @property
    def path(self):
        return self._path

    @property
    def name(self):
        return self._name

    @property
    def dtype(self):
        return self._dtype

    @property
    def gmm(self):
        return self._gmm

    @property
    def is_fitted(self):
        return self._is_fitted

    def _refresh_T_statistics(self):
        """ depend on: Tm and Sigma """
        self.T_invS = self.Tm / (self.Sigma + EPS)
        T_invS2 = self.Tm / (np.sqrt(self.Sigma) + EPS)
        for mix in range(self.nmix):
            start = self.feat_dim * mix
            end = start + self.feat_dim
            tmp = T_invS2[:, start:end].dot(T_invS2[:, start:end].T)
            self.T_invS_Tt[mix] = tmp[self._itril]

    def _refresh_gpu(self):
        if hasattr(self, '_gpu_inputs'):
            if hasattr(self, '_gpu_outputs'):
                return
        with tf.variable_scope(self.name):
            Z = K.placeholder(shape=(None, self.nmix), dtype=(self.dtype),
              name='ZeroStats')
            F = K.placeholder(shape=(None, self.nmix * self.feat_dim), dtype=(self.dtype),
              name='FirstStats')
            Tm = K.placeholder(shape=(self.Tm.shape), dtype=(self.dtype),
              name='T_matrix')
            T_invS_Tt = K.placeholder(shape=(self.T_invS_Tt.shape), dtype=(self.dtype),
              name='T_invS_Tt')
            Sigma = tf.constant(value=(self.Sigma), dtype=(self.dtype),
              name='GMM_Sigma')
            Im = tf.eye((self.tv_dim), dtype=(self.dtype), name='Im')
            T_invS = Tm / Sigma
            L1 = tf.matmul(Z, T_invS_Tt, name='L1')
            B1 = tf.matmul(F, (tf.transpose(T_invS)), name='B1')
            n_samples = tf.shape(L1)[0]
            IDX = tf.range(start=0, limit=n_samples, dtype='int32')

            def map_expectation_fn(idx):
                l1 = L1[idx]
                b1 = B1[idx]
                L = tf.scatter_nd(indices=[(i, j) for i, j in zip(*self._itril)], updates=l1,
                  shape=(
                 self.tv_dim, self.tv_dim),
                  name='L')
                L = L + tf.transpose(K.tril(L, k=(-1))) + Im
                with tf.device('/cpu:0'):
                    Cxx = tf.linalg.inv(L)
                B = tf.expand_dims(b1, axis=(-1))
                this_Ex = tf.matmul(Cxx, B)
                Ex = tf.transpose(this_Ex)
                llk = -0.5 * tf.matmul(Ex, B - this_Ex) + tf.matmul(Ex, B)
                Exx = tf.gather_nd(params=(Cxx + tf.matmul(this_Ex, Ex)), indices=[(i, j) for i, j in zip(*self._itril)])
                return tf.concat((tf.squeeze(llk, axis=0),
                 tf.squeeze(Ex, axis=0),
                 Exx),
                  axis=0)

            llk_Ex_Exx = tf.map_fn(fn=map_expectation_fn, elems=IDX,
              dtype=(self.dtype),
              parallel_iterations=(self.batch_size_gpu),
              swap_memory=False,
              back_prop=False)
            llk = llk_Ex_Exx[:, 0]
            Ex = llk_Ex_Exx[:, 1:1 + self.tv_dim]
            Exx = llk_Ex_Exx[:, 1 + self.tv_dim:]
            RU = tf.matmul(tf.transpose(Ex), F)
            LU = tf.matmul(tf.transpose(Z), Exx)
            llk = tf.reduce_sum(llk)
            self._gpu_e_inputs = [
             Z, F, Tm, T_invS_Tt]
            self._gpu_e_outputs = [LU, RU, llk]
            self._gpu_t_inputs = self._gpu_e_inputs
            self._gpu_t_outputs = [Ex]
            LU = K.placeholder(shape=(self.nmix, self.t2_dim), dtype=(self.dtype),
              name='LU_plh')
            RU = K.placeholder(shape=(self.tv_dim, self.nmix * self.feat_dim), dtype=(self.dtype),
              name='RU_plh')
            MIX_ID = tf.range(start=0, limit=(self.nmix), dtype='int32')

            def map_maximization_fn(mix):
                lu = tf.scatter_nd(indices=[(i, j) for i, j in zip(*self._itril)], updates=(LU[mix]),
                  shape=(
                 self.tv_dim, self.tv_dim),
                  name='lu')
                lu = lu + tf.transpose(K.tril(lu, k=(-1)))
                ru = RU[:, mix * self.feat_dim:mix * self.feat_dim + self.feat_dim]
                ru.set_shape((self.tv_dim, self.feat_dim))
                with tf.device('/cpu:0'):
                    t = tf.linalg.solve(matrix=lu, rhs=ru, adjoint=False, name=None)
                return t

            Tm = tf.map_fn(fn=map_maximization_fn, elems=MIX_ID,
              dtype=(self.dtype),
              parallel_iterations=(self.batch_size_gpu),
              swap_memory=False,
              back_prop=False)
            self._gpu_m_inputs = [LU, RU]
            self._gpu_m_outputs = Tm

    def _fast_expectation(self, Z, F, on_gpu):
        nframes = np.ceil(Z.sum())
        nfiles = F.shape[0]
        if on_gpu:
            LU, RU, llk = K.eval((self._gpu_e_outputs), feed_dict={i:j for i, j in zip(self._gpu_e_inputs, (
             Z, F, self.Tm, self.T_invS_Tt))})
            return (
             LU, RU, llk, nframes)
        else:
            L1 = np.dot(Z, self.T_invS_Tt)
            B1 = np.dot(F, self.T_invS.T)
            Ex, Exx, llk = self._Ex_Exx_llk[nfiles]
            for ix in range(nfiles):
                L = np.zeros((self.tv_dim, self.tv_dim), dtype=(self.dtype))
                L[self._itril] = L1[ix]
                L = L + np.tril(L, k=(-1)).T + self.Im
                Cxx = linalg.inv(L)
                B = B1[ix][:, np.newaxis]
                this_Ex = np.dot(Cxx, B)
                this_ExT = this_Ex.T
                Ex[ix] = this_ExT
                llk[ix] = -0.5 * this_ExT.dot(B - this_Ex) + this_ExT.dot(B)
                Exx[ix] = (Cxx + this_Ex.dot(this_ExT))[self._itril]

            RU = np.dot(Ex.T, F)
            LU = np.dot(Z.T, Exx)
            return (LU, RU, llk.sum(), nframes)

    def expectation(self, Z, F, device=None, print_progress=True):
        """
    Return
    ------
    LU : numpy.ndarray (tdim, nmix * feat_dim)
    RU : numpy.ndarray (nmix, tdim * (tdim + 1) / 2)
    llk : scalar (float)
    nframes : scalar (int)
    """
        if device is None:
            device = self._device
        nfiles = Z.shape[0]
        if nfiles <= self.batch_size_cpu and device == 'cpu' or nfiles <= self.batch_size_gpu and device in ('mix',
                                                                                                             'gpu'):
            return self._fast_expectation(Z=Z, F=F, on_gpu=(False if device == 'cpu' else True))
        else:

            def _map_expectation(start, end, on_gpu):
                batch_size = self.batch_size_gpu if on_gpu else self.batch_size_cpu
                for s, e in batching(n=(end - start), batch_size=batch_size):
                    s += start
                    e += start
                    nfiles = e - s
                    yield (self._fast_expectation(Z=(Z[s:e]), F=(F[s:e]), on_gpu=on_gpu),
                     nfiles)

            def _mpi_fn(start_end):
                start, end = start_end
                tmp = [0.0, 0.0, 0.0, 0.0]
                for res, nfiles in _map_expectation(start, end, on_gpu=False):
                    yield nfiles
                    for i, r in enumerate(res):
                        tmp[i] += r

                size = array_size(tmp[0]) / 1073741824
                if size > 1:
                    tmp[0] = tmp[0].astype('float32')
                else:
                    if size > 2:
                        tmp[0] = tmp[0].astype('float16')
                    size = array_size(tmp[1]) / 1073741824
                    if size > 1:
                        tmp[1] = tmp[1].astype('float32')
                    elif size > 2:
                        tmp[1] = tmp[1].astype('float16')
                yield tmp

            def _thread_fn(start_end):
                start, end = start_end
                tmp = [0.0, 0.0, 0.0, 0.0]
                for res, nfiles in _map_expectation(start, end, on_gpu=True):
                    results.update(nfiles)
                    for i, r in enumerate(res):
                        tmp[i] += r

                results.update(tmp)

            jobs_cpu, jobs_gpu = _split_jobs(n_samples=nfiles, ncpu=(self.ncpu), device=device,
              gpu_factor=(self.gpu_factor))
            results = _ExpectationResults(n_samples=nfiles, nb_results=4, name=('[Tmatrix] Tdim:%d nmix:%d feat_dim:%d iter:%d' % (
             self.tv_dim, self.nmix, self.feat_dim,
             len(self._llk_hist) + 1)),
              print_progress=print_progress)
            mpi = MPI(jobs=jobs_cpu, func=_mpi_fn, ncpu=(self.ncpu),
              batch=1,
              hwm=33554432)
            threads = [threading.Thread(target=_thread_fn, args=(j,)) for j in jobs_gpu]
            for t in threads:
                t.start()

            for r in mpi:
                if not is_number(r):
                    r = [i.astype(self.dtype) if i.dtype != self.dtype else i for i in r if isinstance(i, np.ndarray)]
                results.update(r)

            for t in threads:
                t.join()

            return results.stats

    def maximization(self, LU, RU, nframes=None, min_div_est=True, orthogonalize=True):
        self._is_fitted = True
        prog = Progbar(target=(self.nmix), print_report=True,
          print_summary=False,
          name=('[Tmatrix] Maximization #mix:%d #iter:%d device:%s' % (
         self.nmix, len(self._llk_hist),
         'CPU' if self.device == 'cpu' else 'GPU')))
        if self.device == 'cpu':
            for mix in range(self.nmix):
                prog.add(1)
                lu = np.zeros((self.tv_dim, self.tv_dim), dtype=(self.dtype))
                lu[self._itril] = LU[mix, :]
                lu += np.tril(lu, -1).T
                start = self.feat_dim * mix
                end = start + self.feat_dim
                self.Tm[:, start:end] = linalg.solve(lu, RU[:, start:end])

        else:
            Tm = K.eval((self._gpu_m_outputs), feed_dict={i:j for i, j in zip(self._gpu_m_inputs, (
             LU, RU))})
            for mix, solution in enumerate(Tm):
                start = self.feat_dim * mix
                end = start + self.feat_dim
                self.Tm[:, start:end] = solution

        if min_div_est:
            if nframes is None:
                raise ValueError('`nframes` must be specified if `min_div_est=True`')
            lu = np.zeros((self.tv_dim, self.tv_dim))
            lu[self._itril] = LU.sum(0) / nframes
            lu += np.tril(lu, -1).T
            self.Tm = np.dot(linalg.cholesky(lu), self.Tm)
        if orthogonalize:
            U_, s_, V_ = linalg.svd((self.Tm), full_matrices=False)
            self.Tm = np.diag(s_).dot(V_)
        self.Tm = self.Tm.astype(self.dtype)
        self._refresh_T_statistics()
        return self

    def expectation_maximization(self, Z, F, device=None, print_progress=True):
        nfiles = Z.shape[0]
        start_time = time.time()
        LU, RU, LLK, nframes = self.expectation(Z=Z, F=F, device=device, print_progress=print_progress)
        time_Estep = time.time() - start_time
        start_time = time.time()
        self.maximization(LU, RU, nframes, min_div_est=True,
          orthogonalize=True)
        time_Mstep = time.time() - start_time
        LLK = LLK / nfiles
        self._llk_hist.append(LLK)
        if print_progress:
            print('T-dim:%s #iter:%s llk:%s Estep:%s(s) Mstep:%s(s)' % (
             ctext('%d' % self.tv_dim, 'cyan'),
             ctext('%.2d' % len(self._llk_hist), 'yellow'),
             ctext('%.4f' % LLK, 'yellow'),
             ctext('%.2f' % time_Estep, 'yellow'),
             ctext('%.4f' % time_Mstep, 'yellow')))
        if self.path is not None:
            with open(self.path, 'wb') as (f):
                pickle.dump(self, f)
        return self

    def transform(self, X):
        """ Extract i-vector from trained T-matrix

    Parameters
    ----------
    X : {tuple, list, numpy.ndarray, odin.fuel.data.MmapArray}
      if tuple or list is given, the inputs include:
      Z-[1, nmix]; F-[1, nmix*feat_dim]
      if numpy.ndarray is given, shape must be [n_samples, feat_dim]

    Return
    ------
    I-vector : (1, tv_dim)

    Note
    ----
    No need to parallel this function, `numpy.linalg.inv` is
    already a multi-threaded method, and will be bottleneck
    for `multiprocessing`

    """
        if isinstance(X, (tuple, list)):
            Z, F = X
            assert Z.ndim == 2 and Z.shape[1] == self.nmix, 'Zero-th order statistics must be 2-D matrix, and `Z.shape=[?, %d]; but given: %s' % (
             self.nmix, str(Z.shape))
            assert F.ndim == 2 and F.shape[1] == self.nmix * self.feat_dim, 'First order statistics must be 2-D matrix, and `F.shape=[?, %d]; but given: %s' % (
             self.nmix * self.feat_dim, str(F.shape))
        else:
            Z, F = self.gmm.transform(X)
        L = np.zeros((self.tv_dim, self.tv_dim), dtype=(self.dtype))
        L[self._itril] = np.dot(Z, self.T_invS_Tt)
        L += np.tril(L, -1).T + self.Im
        Cxx = linalg.inv(L)
        B = np.dot(self.T_invS, F.T)
        Ex = np.dot(Cxx, B)
        return Ex.T

    def transform_to_disk(self, Z, F, path=None, dtype='float32', device='gpu', ncpu=None, override=True):
        """ Same as `transform`, however, save the transformed statistics
    to file using `odin.fuel.MmapArray`

    Parameters
    ----------
    Z : {None, numpy.ndarray, odin.fuel.data.MmapArray}
      array of zero-th order statistic [n_samples, nmix]
    F : {None, numpy.ndarray, odin.fuel.data.MmapArray}
      array of first-th order statistic [n_samples, nmix * feat_dim]
    path : {str, None}
      if str, saving path for extracted i-vector, otherwise,
      return numpy.ndarray for the i-vector

    Return
    ------
    i-vector : (1, tv_dim)

    Note
    ----
    this function return i-vectors in the same order provided
    by `Z` and `F`
    Calculation on `gpu` is approximated to the results from
    `cpu` that satisfied `np.allclose(gpu, cpu, rtol=1.e-5, atol=1.e-4)`,
    the final performance using cosine scoring, GMM and PLDA is identical.
    """
        if device is None:
            device = self._device
        else:
            dtype = self.dtype if dtype is None else np.dtype(dtype)
            if Z is not None and F is not None:
                n_samples = Z.shape[0]
                if Z.shape[0] != F.shape[0]:
                    raise ValueError('Number of samples in `Z` is %d which is different from %d samples in `F`' % (
                     Z.shape[0], F.shape[0]))
            else:
                raise ValueError('Input arguments must contain `X` and `indices`, or `Z` and `F`.')
            prog = Progbar(target=n_samples, print_report=True,
              print_summary=True,
              name=('Extracting %d-D i-vector' % self.tv_dim))
            if path is not None:
                if os.path.exists(path):
                    if override:
                        os.remove(path)
                dat = MmapArray(path=path, dtype=dtype, shape=(
                 n_samples, self.tv_dim),
                  read_only=False)
            else:
                dat = np.empty(shape=(n_samples, self.tv_dim), dtype=dtype)
            if (device == 'gpu' or device == 'mix') and get_ngpu() > 0:
                for s, e in batching(batch_size=(self.batch_size_gpu), n=n_samples):
                    z_minibatch = Z[s:e]
                    f_minibatch = F[s:e]
                    Ex = K.eval((self._gpu_t_outputs), feed_dict={i:j for i, j in zip(self._gpu_t_inputs, (
                     z_minibatch, f_minibatch, self.Tm, self.T_invS_Tt))})
                    prog.add(Ex[0].shape[0])
                    dat[s:e] = Ex[0]

            else:

                def extract_ivec(idx):
                    vecs = []
                    for i in idx:
                        L = np.zeros((self.tv_dim, self.tv_dim), dtype=(self.dtype))
                        L[self._itril] = np.dot(Z[i:i + 1], self.T_invS_Tt)
                        L += np.tril(L, -1).T + self.Im
                        Cxx = linalg.inv(L)
                        B = np.dot(self.T_invS, F[i:i + 1].T)
                        Ex = np.dot(Cxx, B)
                        ivec = Ex.T
                        if ivec.dtype != dtype:
                            ivec = ivec.astype(dtype)
                        vecs.append((i, ivec))

                    return vecs

                mpi = MPI(jobs=(list(range(n_samples))), func=extract_ivec, ncpu=(self.ncpu if ncpu is None else int(ncpu)),
                  batch=(max(12, self.batch_size_cpu)))
                for vecs in mpi:
                    for i, v in vecs:
                        dat[i:i + 1] = v

                    prog.add(len(vecs))

        if path is not None:
            dat.flush()
            dat.close()
            return MmapArray(path=path, read_only=True)
        else:
            return dat

    def fit(self, X, y=None):
        """ Extract i-vector from trained T-matrix

    Parameters
    ----------
    X : {tuple, list; or numpy.ndarray}
      if tuple or list is given, the inputs include:
      Z-(1, nmix); F-(1, nmix*feat_dim)
      if numpy.ndarray and indices is given, shape must
      be (n, feat_dim), and the indices is list of dictionary
      representing the mapping: 'name' -> (start, end)
    """
        randID = uuid(length=12)
        cache_Z = os.path.join(self.cache_path, 'Z_%s' % randID)
        cache_F = os.path.join(self.cache_path, 'F_%s' % randID)
        try:
            if not isinstance(X, (tuple, list)):
                if len(X) != 2:
                    raise ValueError('`X` must be tuple or list of length 2.')
            if any(hasattr(i, 'shape') and i.shape[1] == self.feat_dim for i in X):
                if any(isinstance(i, (tuple, list, Mapping)) for i in X):
                    tmp = [i for i in X if hasattr(i, 'shape') if i.shape[1] == self.feat_dim][0]
                    indices = [i for i in X if i != tmp][0]
                    X = tmp
                    self.gmm.transform_to_disk(X, indices, pathZ=cache_Z, pathF=cache_F, dtype='float32',
                      device=None,
                      override=True)
                    Z = MmapArray(cache_Z, read_only=True)
                    F = MmapArray(cache_F, read_only=True)
            elif any(i.shape[1] == self.nmix for i in X):
                if any(i.shape[1] == self.feat_dim * self.nmix for i in X):
                    Z = [i for i in X if i.shape[1] == self.nmix][0]
                    F = [i for i in X if i.shape[1] == self.nmix * self.feat_dim][0]
            else:
                raise ValueError('The input arguments must be tuple of (Z, F) or (X, indices).')
            for iter in range(self.niter):
                self.expectation_maximization(Z, F, device=(self._device), print_progress=True)

        finally:
            if os.path.exists(cache_Z):
                os.remove(cache_Z)
            if os.path.exists(cache_F):
                os.remove(cache_F)