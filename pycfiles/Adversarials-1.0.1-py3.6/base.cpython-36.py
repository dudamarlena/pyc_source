# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/adversarials/core/base.py
# Compiled at: 2018-12-21 01:06:52
# Size of source mod 2**32: 3969 bytes
"""Base classes for Adversarial package.

   @author
     Victor I. Afolabi
     Artificial Intelligence Expert & Software Engineer.
     Email: javafolabi@gmail.com | victor.afolabi@zephyrtel.com
     GitHub: https://github.com/victor-iyiola

   @project
     File: base.py
     Created on 20 December, 2018 @ 06:56 PM.

   @license
     MIT License
     Copyright (c) 2018. Victor I. Afolabi. All rights reserved.
"""
import os.path
from abc import ABCMeta, abstractmethod
from adversarials.core.utils import File, Log
from adversarials.core.consts import FS

class _Base(object):

    def __init__(self, *args, **kwargs):
        self._verbose = kwargs.setdefault('verbose', 1)
        self._name = kwargs.get('name', self.__class__.__name__)

    def __repr__(self):
        """Object representation of Sub-classes."""
        kwargs = self._get_kwargs()
        fmt = ''
        for k, v in kwargs:
            if k in ('captions', 'filename', 'ids'):
                pass
            else:
                fmt += ', {}={!r}'.format(k, v)

        return '{}({})'.format(self.__class__.__name__, fmt.lstrip(', '))

    def __str__(self):
        """String representation of Sub-classes."""
        return '{}()'.format(self.__class__.__name__, ', '.join(map(str, self._get_args())))

    def __format__(self, format_spec):
        if format_spec == '!r':
            return self.__repr__()
        else:
            return self.__str__()

    def _log(self, *args, level: str='log', **kwargs):
        """Logging method helper based on verbosity."""
        if not kwargs.pop('verbose', self._verbose):
            return
        _levels = ('log', 'debug', 'info', 'warn', 'error', 'critical')
        if level.lower() not in _levels:
            raise ValueError('`level` must be one of {}'.format(_levels))
        eval(f"Log.{level.lower()}(*args, **kwargs)")

    def _get_args(self):
        return []

    def _get_kwargs(self):
        return sorted([(k.lstrip('_'), getattr(self, (f"{k}"))) for k in self.__dict__.keys()])

    @property
    def name(self):
        return self._name

    @property
    def verbose(self):
        return self._verbose


class ModelBase(_Base, metaclass=ABCMeta):

    def __init__(self, *args, **kwargs):
        (super(ModelBase, self).__init__)(*args, **kwargs)
        self._cache_dir = kwargs.get('cache_dir', os.path.join(FS.MODEL_DIR, self._name))
        File.make_dirs((self._cache_dir), verbose=(self._verbose))

    def __call__(self, *args, **kwargs):
        return self.call()

    @abstractmethod
    def call(self, *args, **kwargs):
        return NotImplemented

    @staticmethod
    def int_shape(x):
        """Returns the shape of tensor or variable as tuple of int or None entries.

        Args:
            x (Union[tf.Tensor, tf.Variable]): Tensor or variable. hasattr(x, 'shape')

        Returns:
            tuple: A tuple of integers (or None entries).
        """
        try:
            shape = x.shape
            if not isinstance(shape, tuple):
                shape = tuple(shape.as_list())
            return shape
        except ValueError:
            return

    @property
    def cache_dir(self):
        return self._cache_dir