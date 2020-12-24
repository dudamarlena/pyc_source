# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/slab/formats/base.py
# Compiled at: 2016-01-07 05:48:00
# Size of source mod 2**32: 1176 bytes
import abc
from ..core import Directory, Module
__all__ = ('FormatBase', )

class FormatBase(metaclass=abc.ABCMeta):

    def __init__(self, options):
        self.configure(options)

    def render(self, item):
        if isinstance(item, Directory) and item.is_package:
            return self.package(item)
        if isinstance(item, Module):
            return self.module(item)
        raise TypeError('unknown item type: {}'.format(item.__class__))

    @abc.abstractmethod
    def configure(self, options):
        raise NotImplementedError()

    def module(self, module):
        raise NotImplementedError()

    def package(self, package):
        raise NotImplementedError()

    def toc(self, items):
        raise NotImplementedError()

    @classmethod
    @abc.abstractmethod
    def add_arguments(cls, parser):
        raise NotImplementedError()


class MetaFormatBase(FormatBase):

    def __init__(self, options, format_cls):
        self._format = format_cls(options)
        super().__init__(options)

    @property
    def format(self):
        return self._format