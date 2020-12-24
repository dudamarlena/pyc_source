# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: E:\01_Work\15_PhD\11_Python_neural_mass_models\PyRates\pyrates\ir\abc.py
# Compiled at: 2020-01-06 14:08:19
# Size of source mod 2**32: 3271 bytes
__doc__ = '\n'
from typing import Tuple, Iterator, Union
__author__ = 'Daniel Rose'
__status__ = 'Development'

class AbstractBaseIR:
    """AbstractBaseIR"""
    __slots__ = [
     '_template', '_h']

    def __init__(self, template: str=None):
        self._template = template

    @property
    def template(self):
        return self._template

    def __getitem__(self, key: str):
        """
        Custom implementation of __getitem__ that dissolves strings of form "key1/key2/key3" into
        lookups of form self[key1][key2][key3].

        Parameters
        ----------
        key

        Returns
        -------
        item
        """
        if not isinstance(key, str):
            raise TypeError('Keys must be strings of format `key1/key2/...`.')
        key_iter = iter(key.split('/'))
        try:
            key = next(key_iter)
            item = self.getitem_from_iterator(key, key_iter)
            for key in key_iter:
                item = item.getitem_from_iterator(key, key_iter)

        except KeyError as e:
            if hasattr(self, key):
                item = getattr(self, key)
            else:
                raise e

        return item

    def getitem_from_iterator(self, key: str, key_iter: Iterator[str]):
        """Invoked by __getitem__ or [] slicing. Needs to be implemented in subclass."""
        raise NotImplementedError

    def __contains__(self, key):
        try:
            self[key]
        except KeyError:
            return False
        else:
            return True

    def __hash__(self):
        return self._h