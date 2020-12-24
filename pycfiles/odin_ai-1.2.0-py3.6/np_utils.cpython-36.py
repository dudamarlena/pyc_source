# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/odin/utils/np_utils.py
# Compiled at: 2019-01-24 05:01:19
# Size of source mod 2**32: 9489 bytes
from __future__ import division, absolute_import, print_function
import math, marshal, numpy as np, scipy as sp
from six import string_types
__all__ = [
 'array2bytes',
 'bytes2array',
 'one_hot',
 'unique_labels',
 'label_splitter']
idx_2_dt = {b'0':'float32', 
 b'1':'float64',  b'2':'int32', 
 b'3':'int64',  b'4':'bool', 
 b'5':'float16', 
 b'6':'int16',  b'7':'complex64', 
 b'8':'complex128'}
dt_2_idx = {'float32':b'0',  'float64':b'1',  'int32':b'2', 
 'int64':b'3',  'bool':b'4', 
 'float16':b'5', 
 'int16':b'6',  'complex64':b'7', 
 'complex128':b'8'}
nd_2_idx = {0:b'0', 
 1:b'1',  2:b'2',  3:b'3',  4:b'4',  5:b'5', 
 6:b'6',  7:b'7',  8:b'8',  9:b'9',  10:b'10', 
 11:b'11',  12:b'12'}

def array2bytes(a):
    """ Fastest way to convert `numpy.ndarray` and all its
  metadata to bytes array.
  """
    shape = marshal.dumps(a.shape, 0)
    array = a.tobytes() + shape + dt_2_idx[a.dtype.name] + nd_2_idx[a.ndim]
    return array


def bytes2array(b):
    """ Deserialize result from `array2bytes` back to `numpy.ndarray` """
    ndim = int(b[-1:])
    dtype = idx_2_dt[b[-2:-1]]
    i = -((ndim + 1) * 5) - 2
    shape = marshal.loads(b[i:-2])
    return np.frombuffer((b[:i]), dtype=dtype).reshape(shape)


class _LabelsIndexing(object):
    __doc__ = ' LabelsIndexing\n\n  Parameters\n  ----------\n  key_func: callabe\n      a function transform each element of `y` into unique ID\n      for labeling.\n  fast_index: dict\n      mapping from label -> index\n  sorted_labels: list\n      list of all labels, sorted for unique order\n  '

    def __init__(self, key_func, fast_index, sorted_labels):
        super(_LabelsIndexing, self).__init__()
        self._key_func = key_func
        self._fast_index = fast_index
        self._sorted_labels = sorted_labels

    def __call__(self, x):
        x = self._key_func(x)
        if x in self._fast_index:
            return self._fast_index[x]
        raise ValueError("Cannot find key: '%s' in %s" % (
         str(x), str(self._sorted_labels)))


def one_hot(y, nb_classes=None, dtype='float32'):
    """Convert class vector (integers from 0 to nb_classes)
  to binary class matrix, for use with categorical_crossentropy

  Note
  ----
  if any class index in y is smaller than 0, then all of its one-hot
  values is 0.
  """
    if 'int' not in str(y.dtype):
        y = y.astype('int32')
    else:
        if nb_classes is None:
            nb_classes = np.max(y) + 1
        else:
            nb_classes = int(nb_classes)
    return np.eye(nb_classes, dtype=dtype)[y]


def unique_labels(y, key_func=None, return_labels=False):
    """
  Parameters
  ----------
  y: list, tuple, `numpy.ndarray`
      list of object that is label or contain label information.
  key_func: callabe
      a function transform each element of `y` into unique ID for labeling.
  return_labels: bool
      if True, return the ordered labels.

  Returns
  -------
  (call-able, tuple):
      function that transform any object into unique label index
      (optional) list of ordered labels.
  """
    if not isinstance(y, (list, tuple, np.ndarray)):
        raise ValueError('`y` must be iterable (list, tuple, or numpy.ndarray).')
    if key_func is None or not hasattr(key_func, '__call__'):
        key_func = lambda _: str(_)
    sorted_labels = list(sorted(set(key_func(i) for i in y)))
    fast_index = {j:i for i, j in enumerate(sorted_labels)}
    labels_indexing = _LabelsIndexing(key_func, fast_index, sorted_labels)
    if return_labels:
        return (labels_indexing, tuple(sorted_labels))
    else:
        return labels_indexing


_CACHE_SPLITTER = {}

class _label_split_helper(object):

    def __init__(self, pos, delimiter):
        super(_label_split_helper, self).__init__()
        self.pos = pos
        self.delimiter = delimiter

    def __call__(self, x):
        if isinstance(x, string_types):
            return x.split(self.delimiter)[self.pos]
        else:
            if isinstance(x, (tuple, list, np.ndarray)):
                for i in x:
                    if isinstance(i, string_types):
                        return i.split(self.delimiter)[self.pos]

            else:
                raise RuntimeError('Unsupport type=%s for label splitter' % str(type(x)))


def label_splitter(pos, delimiter='/'):
    pos = int(pos)
    delimiter = str(delimiter)
    splitter_id = str(pos) + delimiter
    if splitter_id not in _CACHE_SPLITTER:
        splitter = _label_split_helper(pos, delimiter)
        _CACHE_SPLITTER[splitter_id] = splitter
    return _CACHE_SPLITTER[splitter_id]