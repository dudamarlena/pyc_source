# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/hostedtoolcache/Python/3.8.0/x64/lib/python3.8/site-packages/pyunits/interning.py
# Compiled at: 2019-11-23 19:40:19
# Size of source mod 2**32: 3333 bytes
from typing import Any, Callable, Tuple
import abc
from loguru import logger
from .exceptions import InterningError

class Interned(abc.ABC):
    __doc__ = '\n    Implements the interning pattern. Instances of the same class that are\n    constructed with the same arguments will be regarded as equivalent.\n\n    Note that all the ctor arguments to the wrapped class must be hashable.\n    '
    _PreHashType = Callable[([Any, Any], Tuple)]
    _INSTANCES = {}

    def __init__(self, *args, _expect_creation: bool=False, **kwargs):
        """
        All parameters are ignored except for _expect_creation.
        :param _expect_creation: Basically, if not set to true, this method will
        throw an exception. It is done like this to guard against the user
        accidentally trying to create an interned class normally.
        """
        if not _expect_creation:
            raise InterningError('Please use get() to create a new instance of this class.')

    @classmethod
    def _pre_hash(cls, *args: Any, **kwargs: Any) -> Tuple:
        """
        Specifies a custom transformation to run on the arguments passed to
        get() before hashing. It will be forwarded these arguments directly, and
        return a tuple of some sort. This can be useful to, for example, ignore
        certain arguments.
        :param args: Positional arguments passed to get().
        :param kwargs: Keyword arguments passed to get().
        :return: A tuple of transformed arguments.
        """
        return tuple(args) + tuple(kwargs.values())

    @abc.abstractmethod
    def _init_new(self, *args: Any, **kwargs: Any) -> None:
        """
        Called when we want to initialize a new instance of the derived class.
        It will be forwarded any arguments passed to get().
        :param args: Positional arguments passed to get().
        :param kwargs: Keyword arguments passed to get().
        """
        pass

    @classmethod
    def get(cls, *args: Any, **kwargs: Any) -> 'Interned':
        """
        Gets an instance of the derived class, returning a cached one if deemed
        appropriate.
        :param args: Will be forwarded to _init_new.
        :param kwargs: Will be forwarded to _init_new.
        :return: The instance that it created.
        """
        arg_signature = (cls._pre_hash)(*args, **kwargs)
        signature = (
         cls, arg_signature)
        instance = cls._INSTANCES.get(signature)
        if instance is None:
            logger.debug('Creating new canonical instance: {}', signature)
            instance = cls(_expect_creation=True)
            (instance._init_new)(*args, **kwargs)
            cls._INSTANCES[signature] = instance
        return instance

    @classmethod
    def clear_interning_cache(cls) -> None:
        """
        Forcefully clears any cached instances. This is mostly useful for
        testing, where we want to force it to create a new instance every time.
        """
        cls._INSTANCES = {}