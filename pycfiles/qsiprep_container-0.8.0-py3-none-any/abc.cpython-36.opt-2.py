# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/circleci/.pyenv/versions/3.6.5/lib/python3.6/abc.py
# Compiled at: 2019-03-22 00:31:38
# Size of source mod 2**32: 10782 bytes
from . import _bootstrap
from . import _bootstrap_external
from . import machinery
try:
    import _frozen_importlib
except ImportError as exc:
    if exc.name != '_frozen_importlib':
        raise
    _frozen_importlib = None

try:
    import _frozen_importlib_external
except ImportError as exc:
    _frozen_importlib_external = _bootstrap_external

import abc

def _register(abstract_cls, *classes):
    for cls in classes:
        abstract_cls.register(cls)
        if _frozen_importlib is not None:
            try:
                frozen_cls = getattr(_frozen_importlib, cls.__name__)
            except AttributeError:
                frozen_cls = getattr(_frozen_importlib_external, cls.__name__)

            abstract_cls.register(frozen_cls)


class Finder(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def find_module(self, fullname, path=None):
        pass


class MetaPathFinder(Finder):

    def find_module(self, fullname, path):
        if not hasattr(self, 'find_spec'):
            return
        found = self.find_spec(fullname, path)
        if found is not None:
            return found.loader

    def invalidate_caches(self):
        pass


_register(MetaPathFinder, machinery.BuiltinImporter, machinery.FrozenImporter, machinery.PathFinder, machinery.WindowsRegistryFinder)

class PathEntryFinder(Finder):

    def find_loader(self, fullname):
        if not hasattr(self, 'find_spec'):
            return (None, [])
        else:
            found = self.find_spec(fullname)
            if found is not None:
                if not found.submodule_search_locations:
                    portions = []
                else:
                    portions = found.submodule_search_locations
                return (
                 found.loader, portions)
            return (None, [])

    find_module = _bootstrap_external._find_module_shim

    def invalidate_caches(self):
        pass


_register(PathEntryFinder, machinery.FileFinder)

class Loader(metaclass=abc.ABCMeta):

    def create_module(self, spec):
        pass

    def load_module(self, fullname):
        if not hasattr(self, 'exec_module'):
            raise ImportError
        return _bootstrap._load_module_shim(self, fullname)

    def module_repr(self, module):
        raise NotImplementedError


class ResourceLoader(Loader):

    @abc.abstractmethod
    def get_data(self, path):
        raise IOError


class InspectLoader(Loader):

    def is_package(self, fullname):
        raise ImportError

    def get_code(self, fullname):
        source = self.get_source(fullname)
        if source is None:
            return
        else:
            return self.source_to_code(source)

    @abc.abstractmethod
    def get_source(self, fullname):
        raise ImportError

    @staticmethod
    def source_to_code(data, path='<string>'):
        return compile(data, path, 'exec', dont_inherit=True)

    exec_module = _bootstrap_external._LoaderBasics.exec_module
    load_module = _bootstrap_external._LoaderBasics.load_module


_register(InspectLoader, machinery.BuiltinImporter, machinery.FrozenImporter)

class ExecutionLoader(InspectLoader):

    @abc.abstractmethod
    def get_filename(self, fullname):
        raise ImportError

    def get_code(self, fullname):
        source = self.get_source(fullname)
        if source is None:
            return
        try:
            path = self.get_filename(fullname)
        except ImportError:
            return self.source_to_code(source)
        else:
            return self.source_to_code(source, path)


_register(ExecutionLoader, machinery.ExtensionFileLoader)

class FileLoader(_bootstrap_external.FileLoader, ResourceLoader, ExecutionLoader):
    pass


_register(FileLoader, machinery.SourceFileLoader, machinery.SourcelessFileLoader)

class SourceLoader(_bootstrap_external.SourceLoader, ResourceLoader, ExecutionLoader):

    def path_mtime(self, path):
        if self.path_stats.__func__ is SourceLoader.path_stats:
            raise IOError
        return int(self.path_stats(path)['mtime'])

    def path_stats(self, path):
        if self.path_mtime.__func__ is SourceLoader.path_mtime:
            raise IOError
        return {'mtime': self.path_mtime(path)}

    def set_data(self, path, data):
        pass


_register(SourceLoader, machinery.SourceFileLoader)