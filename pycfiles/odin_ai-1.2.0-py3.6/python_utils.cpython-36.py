# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/odin/utils/python_utils.py
# Compiled at: 2019-09-16 09:25:24
# Size of source mod 2**32: 14704 bytes
from __future__ import absolute_import, division, print_function
import inspect, io, numbers, os, re, string, tarfile, types, warnings
from collections import Iterable, Iterator, Mapping, OrderedDict, defaultdict, deque
from contextlib import contextmanager
from datetime import datetime
import numpy as np
from six import add_metaclass, string_types
from six.moves import cPickle
GZIP_MAGIC_NUMBER = '1f8b'

def is_gzip_file(path):
    """ Credit:
  https://kite.com/python/examples/4945/gzip-check-if-a-file-is-gzip-compressed
  """
    if isinstance(path, string_types):
        if os.path.isfile(path):
            with open(path, 'rb') as (f):
                return f.read(2).encode('hex') == GZIP_MAGIC_NUMBER
    if hasattr(path, 'read') and hasattr(path, 'tell'):
        last_pos = path.tell()
        path.seek(0)
        indicator = path.read(2)
        indicator = indicator.encode('hex') if isinstance(indicator, string_types) else indicator.hex()
        path.seek(last_pos)
        return indicator == GZIP_MAGIC_NUMBER
    else:
        return False


def is_tar_file(path):
    if not os.path.isfile(path):
        return False
    else:
        return tarfile.is_tarfile(path)


RE_NUMBER = re.compile('^[+-]*((\\d*\\.\\d+)|(\\d+))$')

def get_formatted_datetime(only_number=True):
    if only_number:
        return '{:%H%M%S%d%m%y}'.format(datetime.now())
    else:
        return '{:%H:%M:%S-%d%b%y}'.format(datetime.now())


def get_all_properties(obj):
    """ Return all attributes which are properties of given Object
  """
    properties = []
    clazz = obj if isinstance(obj, type) else obj.__class__
    for key in dir(clazz):
        if '__' in key:
            pass
        else:
            val = getattr(clazz, key)
            if isinstance(val, property):
                properties.append(key)

    if isinstance(obj, type):
        return properties
    else:
        return {p:getattr(obj, p) for p in properties}


def get_string_placeholders(s):
    assert isinstance(s, string_types)
    fmt = []
    for _, key, spec, _ in string.Formatter().parse(save_path):
        if spec is not None:
            fmt.append(key)

    return tuple(fmt)


def as_tuple(x, N=None, t=None):
    """
  Coerce a value to a tuple of given length (and possibly given type).

  Parameters
  ----------
  x : {value, iterable}
  N : {integer}
      length of the desired tuple
  t : {type, call-able, optional}
      required type for all elements

  Returns
  -------
  tuple
      ``tuple(x)`` if `x` is iterable, ``(x,) * N`` otherwise.

  Raises
  ------
  TypeError
      if `type` is given and `x` or any of its elements do not match it
  ValueError
      if `x` is iterable, but does not have exactly `N` elements

  Note
  ----
  This function is adpated from Lasagne
  Original work Copyright (c) 2014-2015 lasagne contributors
  All rights reserved.

  LICENSE: https://github.com/Lasagne/Lasagne/blob/master/LICENSE
  """
    if not isinstance(x, tuple):
        if isinstance(x, (types.GeneratorType, list)):
            x = tuple(x)
        else:
            x = (
             x,)
    else:
        if is_number(N):
            N = int(N)
            if len(x) == 1:
                x = x * N
            elif len(x) != N:
                raise ValueError('x has length=%d, but required length N=%d' % (
                 len(x), N))
        else:
            if t is None:
                filter_func = lambda o: True
            else:
                if isinstance(t, type) or isinstance(t, (tuple, list)):
                    filter_func = lambda o: isinstance(o, t)
                else:
                    if hasattr(t, '__call__'):
                        filter_func = t
                    else:
                        raise ValueError('Invalid value for `t`: %s' % str(t))
        raise all(filter_func(v) for v in x) or TypeError('expected a single value or an iterable of {0}, got {1} instead'.format(t.__name__, x))
    return x


def as_list(x, N=None, t=None):
    return list(as_tuple(x, N, t))


def as_bytes(x, nbytes=None, order='little'):
    """ Convert some python object to bytes array, support type:
  * string, unicode
  * integer
  * numpy.ndarray

  Note
  ----
  This method is SLOW
  """
    if is_string(x):
        return x.encode()
    else:
        if isinstance(x, int):
            return x.to_bytes(nbytes, order, signed=False)
        if isinstance(x, np.ndarray):
            return x.tobytes()
    raise ValueError('Not support bytes conversion for type: %s' % type(x).__name__)


def is_lambda(v):
    LAMBDA = lambda : 0
    return isinstance(v, type(LAMBDA)) and v.__name__ == LAMBDA.__name__


def is_pickleable(x):
    try:
        cPickle.dumps(x, protocol=(cPickle.HIGHEST_PROTOCOL))
        return True
    except cPickle.PickleError:
        return False


def is_fileobj(f):
    """ Check if an object `f` is intance of FileIO object created
  by `open()`"""
    return isinstance(f, io.TextIOBase) or isinstance(f, io.BufferedIOBase) or isinstance(f, io.RawIOBase) or isinstance(f, io.IOBase)


def is_callable(x):
    return hasattr(x, '__call__')


def is_string(s):
    return isinstance(s, string_types)


def is_path(path):
    if is_string(path):
        try:
            os.path.exists(path)
            return True
        except Exception as e:
            return False

    return False


def is_number(i, string_number=False):
    if isinstance(i, string_types):
        if string_number:
            return RE_NUMBER.match(i) is not None
    return isinstance(i, numbers.Number)


def is_bool(b):
    return isinstance(b, type(True))


def is_primitives(x, inc_ndarray=True, exception_types=[]):
    """Primitive types include: number, string, boolean, None
  and numpy.ndarray (optional) and numpy.generic (optional)

  Parameters
  ----------
  inc_ndarray: bool
      if True, include `numpy.ndarray` and `numpy.generic` as a primitive types
  """
    if isinstance(x, (tuple, list)):
        return all(is_primitives(i, inc_ndarray=inc_ndarray, exception_types=exception_types) for i in x)
    else:
        if isinstance(x, Mapping):
            return all(is_primitives(i, inc_ndarray=inc_ndarray, exception_types=exception_types) and is_primitives(j, inc_ndarray=inc_ndarray, exception_types=exception_types) for i, j in x.items())
        if is_number(x) or is_string(x) or is_bool(x) or x is None or any(isinstance(x, t) for t in exception_types) or inc_ndarray and isinstance(x, (np.ndarray, np.generic)):
            return True
        return False


def savetxt(fname, X, fmt='%g', delimiter=' ', newline='\n', header='', footer='', index=None, comments='# ', encoding=None, async_backend='thread'):
    """ Save an array to a text file.

  Parameters
  ----------

  fname : filename or file handle
      If the filename ends in .gz, the file is automatically saved
      in compressed gzip format. loadtxt understands gzipped files
      transparently.

  X : 1D or 2D array_like
      Data to be saved to a text file.

  fmt : str or sequence of strs, optional
      A single format (%10.5f), a sequence of formats, or a multi-format
      string, e.g. ‘Iteration %d – %10.5f’, in which case delimiter is
      ignored. For complex X, the legal options for fmt are:

      a single specifier, fmt=’%.4e’, resulting in numbers formatted like
      ‘ (%s+%sj)’ % (fmt, fmt)
      a full string specifying every real and imaginary part, e.g.
      ‘ %.4e %+.4ej %.4e %+.4ej %.4e %+.4ej’ for 3 columns
      a list of specifiers, one per column - in this case, the real and
      imaginary part must have separate specifiers,
      e.g. [‘%.3e + %.3ej’, ‘(%.15e%+.15ej)’] for 2 columns

  delimiter : str, optional
      String or character separating columns.

  newline : str, optional
      String or character separating lines.

  header : str, optional
      String that will be written at the beginning of the file.

  footer : str, optional
      String that will be written at the end of the file.

  comments : str, optional
      String that will be prepended to the header and footer strings, to mark them as comments. Default: ‘# ‘, as expected by e.g. numpy.loadtxt.

  encoding : {None, str}, optional
      Encoding used to encode the outputfile. Does not apply to output streams. If the encoding is something other than ‘bytes’ or ‘latin1’ you will not be able to load the file in NumPy versions < 1.14. Default is ‘latin1’.

  async_backend : {'thread', 'process', None}
      save the data to disk asynchronously using multi-threading or
      multi-processing
  """
    pass


_space_char = re.compile('\\s')
_multiple_spaces = re.compile('\\s\\s+')
_non_alphanumeric_char = re.compile('\\W')

def string_normalize(text, lower=True, remove_non_alphanumeric=True, remove_duplicated_spaces=True, remove_whitespace=False, escape_pattern=False):
    text = str(text).strip()
    if bool(lower):
        text = text.lower()
    if bool(escape_pattern):
        text = re.escape(text)
    if bool(remove_non_alphanumeric):
        text = _non_alphanumeric_char.sub(' ', text)
        text = text.strip()
    if bool(remove_duplicated_spaces):
        text = _multiple_spaces.sub(' ', text)
    if bool(remove_whitespace):
        if isinstance(remove_whitespace, string_types):
            text = _space_char.sub(remove_whitespace, text)
        else:
            text = _space_char.sub('', text)
    return text


text_normalize = string_normalize

def unique(seq, keep_order=False):
    if keep_order:
        seen = set()
        seen_add = seen.add
        return [x for x in seq if x not in seen if not seen_add(x)]
    else:
        return list(set(seq))


class defaultdictkey(defaultdict):
    __doc__ = ' Enhanced version of `defaultdict`, instead of return a\n  default value, return an "improvised" default value based on\n  the given key.\n\n  Example\n  -------\n  >>> from odin.utils.python_utils import defaultdictkey\n  >>> d = defaultdictkey(lambda x: str(x))\n  >>> print(d[\'123\']) # \'123\'\n  '

    def __missing__(self, key):
        if self.default_factory is None:
            raise KeyError(key)
        else:
            ret = self[key] = self.default_factory(key)
            return ret


def multikeysdict(d):
    assert isinstance(d, dict)
    new_d = d.__class__()
    for i, j in d.items():
        if isinstance(i, tuple):
            for k in i:
                new_d[k] = j

        else:
            new_d[i] = j

    return new_d


class abstractclassmethod(classmethod):
    __isabstractmethod__ = True

    def __init__(self, method):
        method.__isabstractmethod__ = True
        super(abstractclassmethod, self).__init__(method)


class classproperty(object):

    def __init__(self, fn):
        super(classproperty, self).__init__()
        self.fn = fn

    def __get__(self, obj, owner):
        return self.fn(owner)


def select_path(*paths, default=None, create_new=False):
    """
  Parameters
  ----------
  paths : str
    multiple path are given

  default : str
    default path for return

  create_new : bool (default: False)
    if no path is found, create new folder based on the
    first path found to be `creat-able`
  """
    all_paths = []
    for p in paths:
        if isinstance(p, (tuple, list)):
            all_paths += p
        else:
            if isinstance(p, string_types):
                all_paths.append(p)
            else:
                raise ValueError("Given `path` has type: '%s', which must be string or list of string")

    for p in all_paths:
        if os.path.exists(p):
            return p

    if default is not None:
        return str(default)
    if create_new:
        for p in paths:
            base_dir = os.path.dirname(p)
            if os.path.exists(base_dir):
                os.mkdir(p)
                return p

        raise ValueError('Cannot create new folder from list: %s' % str(paths))
    raise RuntimeError('Cannot find any exists path from list: %s' % '; '.join(all_paths))


@contextmanager
def catch_warnings_error(w):
    """ This method turn any given warnings into exception

  use: `warnings.Warning` for all warnings

  Example
  -------
  >>> with catch_warnings([RuntimeWarning, UserWarning]):
  >>>   try:
  >>>     warnings.warn('test', category=RuntimeWarning)
  >>>   except RuntimeWarning as w:
  >>>     pass
  """
    with warnings.catch_warnings():
        warnings.filterwarnings(action='error', category=w)
        yield


@contextmanager
def catch_warnings_ignore(w):
    """ This method ignore any given warnings

  use: `warnings.Warning` for all warnings
  """
    with warnings.catch_warnings():
        warnings.filterwarnings(action='ignore', category=w)
        yield