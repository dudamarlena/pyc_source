# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\expatriate\model\Mapper.py
# Compiled at: 2018-01-18 12:27:50
# Size of source mod 2**32: 1919 bytes
import importlib, logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class Mapper(object):
    __doc__ = '\n    Super class of Mapper types. Defines the methods to be overriden and a few\n    convenience methods.\n    '

    def __init__(self, **kwargs):
        self._kwargs = kwargs

    def __str__(self):
        return self.__class__.__name__ + ' ' + str(self._kwargs)

    def _load_cls(self, cls_):
        """
        Wrapper function to either return cls_ if it is a class or load the
        class if it is a tuple of the form (package, class_name)
        """
        if isinstance(cls_, tuple):
            mod = importlib.import_module(cls_[0])
            return getattr(mod, cls_[1])
        else:
            return cls_

    def initialize(self, *args, **kwargs):
        raise NotImplementedError

    def matches(self, *args, **kwargs):
        raise NotImplementedError

    def parse_in(self, *args, **kwargs):
        raise NotImplementedError

    def validate(self, *args, **kwargs):
        raise NotImplementedError

    def produce_in(self, *args, **kwargs):
        raise NotImplementedError