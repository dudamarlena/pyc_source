# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ana/dev/dexy-clean/dexy/filters/pydoc.py
# Compiled at: 2020-03-18 15:12:33
# Size of source mod 2**32: 6602 bytes
from dexy.exceptions import InternalDexyProblem
from dexy.exceptions import UserFeedback
from dexy.filter import DexyFilter
import imp, inspect, json, os, pkgutil, sqlite3, sys
try:
    from unittest.case import SkipTest
except ImportError:

    class SkipTest(Exception):
        __doc__ = 'Raise this exception to mark a test as skipped.\n        '


class add_workspace_to_sys_path(object):

    def __init__(self, *dirs):
        self.additional_dirs = dirs

    def __enter__(self):
        for dirname in self.additional_dirs:
            sys.path.append(dirname)

    def __exit__(self, type, value, traceback):
        for dirname in self.additional_dirs:
            sys.path.remove(dirname)


class PythonIntrospection(DexyFilter):
    __doc__ = '\n    Base class for classes which use python introspection.\n    '
    import_err_msg = "Could not import '%s' received err: %s"
    aliases = []
    _settings = {'error-on-import-fail':('Should an exception be raised if importing a specified module or file fails?', False), 
     'input-extensions':[
      '.txt', '.py'], 
     'skip-setup-py':('Whether to skip files named setup.py', True), 
     'data-type':'keyvalue', 
     'output-extensions':[
      '.sqlite3', '.json']}

    def handle_fail(self, name, e):
        msg = self.import_err_msg % (name, e)
        if self.setting('error-on-import-fail'):
            raise UserFeedback(msg)
        else:
            self.log_debug(e)

    def load_module(self, name):
        try:
            __import__(name)
            return sys.modules[name]
        except (ImportError, TypeError) as e:
            try:
                self.handle_fail(name, e)
            finally:
                e = None
                del e

    def load_source_file(self):
        self.populate_workspace()
        with add_workspace_to_sys_path(self.workspace(), self.parent_work_dir()):
            name = self.input_data.name
            target = os.path.join(self.workspace(), name)
            if name == 'setup.py':
                if self.setting('skip-setup-py'):
                    self.log_info('Skipping file %s because skip-setup-py is true.' % target)
                    return
            try:
                return imp.load_source('dummy', target)
            except (ImportError, SkipTest) as e:
                try:
                    self.handle_fail(name, e)
                finally:
                    e = None
                    del e


class Pydoc(PythonIntrospection):
    __doc__ = '\n    Returns introspected python data in key-value storage format.\n\n    Where input is a .txt file, this is assumed to be the name of an installed\n    python module.\n\n    Where input is a .py file, the file itself is loaded and parsed.\n    '
    aliases = ['pydoc']
    _settings = {'additional-dirs': ('Additional source directories to load, relative to package root. Useful for tests/', [])}

    def append_item_content(self, key, item):
        self.log_debug('appending content for %s' % key)
        try:
            source = inspect.getsource(item)
            self.output_data.append('%s:source' % key, source)
        except (TypeError, IOError, sqlite3.ProgrammingError):
            pass

        try:
            doc = inspect.getdoc(item)
            self.output_data.append('%s:doc' % key, doc)
        except (TypeError, IOError, sqlite3.ProgrammingError):
            pass

        try:
            comment = inspect.getcomments(item)
            self.output_data.append('%s:comments' % key, comment)
        except (TypeError, IOError, sqlite3.ProgrammingError):
            pass

        try:
            value = json.dumps(item)
            self.output_data.append('%s:value' % key, value)
        except TypeError:
            pass

    def is_defined_in_module(self, mod, mod_name, item):
        if mod_name:
            if hasattr(item, '__module__'):
                return item.__module__.startswith(mod_name)
        return True

    def process_members(self, mod):
        mod_name = mod.__name__
        if mod_name == 'dummy':
            mod_name = None
        for k, m in inspect.getmembers(mod):
            if mod_name:
                key = '%s.%s' % (mod_name, k)
            else:
                key = k
            is_class = inspect.isclass(m)
            is_def = self.is_defined_in_module(mod, mod_name, m)
            if not is_def:
                self.log_debug('skipping %s for module %s' % (k, mod_name))
                continue
            if not is_class:
                self.append_item_content(key, m)
            else:
                self.append_item_content(key, m)
                for ck, cm in inspect.getmembers(m):
                    self.append_item_content('%s.%s' % (key, ck), cm)

    def process_module(self, package_name, name):
        self.log_debug('processing module %s' % name)
        mod = self.load_module(name)
        self.append_item_content(name, mod)
        if mod:
            self.process_members(mod)
        else:
            self.log_warn('no mod from %s' % name)

    def process_package(self, package):
        """
        Iterates over all modules included in the package and processes them.
        """
        self.log_debug('processing package %s' % package)
        package_name = package.__name__
        self.process_module(package_name, package_name)
        if hasattr(package, '__path__'):
            path = package.__path__
            prefix = '%s.' % package_name
            for loader, name, ispkg in pkgutil.walk_packages(path, prefix=prefix):
                self.process_module(package_name, name)

    def process_packages(self):
        package_names = str(self.input_data).split()
        packages = [__import__(name) for name in package_names]
        for package in packages:
            self.process_package(package)

    def process_file(self):
        mod = self.load_source_file()
        if mod:
            self.process_members(mod)

    def process(self):
        if self.prev_ext == '.txt':
            self.process_packages()
        else:
            if self.prev_ext == '.py':
                self.process_file()
            else:
                raise InternalDexyProblem('Should not have ext %s' % self.prev_ext)
        self.output_data.save()