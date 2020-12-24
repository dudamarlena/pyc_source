# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/will/projects/moya/moya/importer.py
# Compiled at: 2016-12-08 16:29:22
from __future__ import unicode_literals
import sys, imp, marshal
from .tags.service import ServiceCallElement
from .document import Document
from .elements.registry import ElementRegistry
from .compat import iteritems
from fs.path import combine, abspath
from fs.errors import NoSysPath
from . import expose
from . import errors

class LibraryImportHook(object):
    _VALID_MODULE_TYPES = set((imp.PY_SOURCE, imp.PY_COMPILED))

    def __init__(self, fs):
        self.fs = fs
        self.module_info = {}
        self._files = set(fs.walk.files())

    def install(self):
        if self not in sys.meta_path:
            sys.meta_path.append(self)

    def uninstall(self):
        try:
            sys.meta_path.remove(self)
        except ValueError:
            pass

    def _get_path(self, fullname):
        if fullname == b'__moyapy__':
            return b'/'
        _, path = fullname.split(b'.', 1)
        path = abspath(path.replace(b'.', b'/'))
        return path

    def _get_module_info(self, fullname):
        if not fullname.startswith(b'__moyapy__'):
            raise ImportError(fullname)
        path = self._get_path(fullname)
        module_path, _type = self._find_module_file(path)
        if module_path is not None:
            return (module_path, _type, False)
        else:
            module_path, _type = self._find_module_file(combine(path, b'__init__'))
            if module_path is not None:
                return (module_path, _type, True)
            raise ImportError(fullname)
            return

    def get_module_info(self, fullname):
        if fullname in self.module_info:
            return self.module_info[fullname]
        module_info = self._get_module_info(fullname)
        self.module_info[fullname] = module_info
        return module_info

    def _find_module_file(self, path):
        for suffix, mode, type in imp.get_suffixes():
            if type in self._VALID_MODULE_TYPES:
                check_path = path + suffix
                if check_path in self._files:
                    return (check_path, type)

        return (None, None)

    def find_module(self, fullname, path=None):
        try:
            self.get_module_info(fullname)
        except ImportError:
            return

        return self
        return

    def is_package(self, fullname, info=None):
        """Check whether the specified module is a package."""
        if info is None:
            info = self.get_module_info(fullname)
        path, type, ispkg = info
        return ispkg

    def get_filename(self, fullname, info=None):
        """Get the __file__ attribute for the specified module."""
        if info is None:
            info = self.get_module_info(fullname)
        path, type, ispkg = info
        if self.fs.hassyspath(path):
            path = self.fs.getsyspath(path)
        return path

    def load_module(self, fullname):
        """Load the specified module.

        This method locates the file for the specified module, loads and
        executes it and returns the created module object.
        """
        info = self.get_module_info(fullname)
        code = self.get_code(fullname, info)
        if code is None:
            raise ImportError(fullname)
        mod = imp.new_module(fullname)
        mod.__file__ = self.get_filename(fullname, info)
        mod.__loader__ = self
        sys.modules[fullname] = mod
        try:
            exec code in mod.__dict__
            if self.is_package(fullname, info):
                mod.__path__ = []
            return mod
        except Exception:
            sys.modules.pop(fullname, None)
            raise

        return

    def get_code(self, fullname, info=None):
        """Get the bytecode for the specified module."""
        if info is None:
            info = self._get_module_info(fullname)
        path, type, ispkg = info
        code = self.fs.getbytes(path)
        if type == imp.PY_SOURCE:
            code = (b'\n').join(code.splitlines())
            try:
                path = self.fs.getsyspath(path)
            except NoSysPath:
                pass

            return compile(code, path, b'exec')
        else:
            if type == imp.PY_COMPILED:
                if code[:4] != imp.get_magic():
                    return
                return marshal.loads(code[8:])
            return code


def fs_import(lib, fs, name):
    hook = LibraryImportHook(fs)
    try:
        ElementRegistry.push_registry(lib.archive.registry)
        hook.install()
        expose.exposed_elements.clear()
        expose.exposed_filters.clear()
        module_name = b'__moyapy__.' + name
        if module_name in sys.modules:
            del sys.modules[module_name]
        try:
            module = __import__(module_name)
        except ImportError as e:
            raise errors.StartupFailedError((b"import error raised for Python extension '{}' ({})").format(name, e), diagnosis=b'This error can occur if an extension has a missing dependency.\n\nYou may need to pip install something.')

        add_module = getattr(module, name)
        lib.py[name] = add_module
        for element_name, element_callable in iteritems(expose.exposed_elements):
            document = Document(lib.archive, lib=lib)
            element = ServiceCallElement(lib.archive, element_name, element_callable, document)
            lib.documents.append(document)
            lib.register_element(element)
            lib.register_named_element(element_name, element)

        lib.filters.update(expose.exposed_filters)
        expose.exposed_elements.clear()
        expose.exposed_filters.clear()
    finally:
        ElementRegistry.pop_registry()
        hook.uninstall()


if __name__ == b'__main__':
    from fs.opener import open_fs
    m = open_fs(b'mem://')
    m.createfile(b'__init__.py')
    m.makedir(b'test')
    m.setbytes(b'test/__init__.py', b'print "Imported!"\ndef run():print "It Works!"')
    m.tree()
    hook = LibraryImportHook(m)
    hook.install()
    module = __import__(b'__moyapy__.test')
    module.test.run()