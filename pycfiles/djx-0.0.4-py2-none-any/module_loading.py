# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-n_sfyb/Django/django/utils/module_loading.py
# Compiled at: 2019-02-14 00:35:17
import copy, os, sys
from importlib import import_module
from django.utils import six

def import_string(dotted_path):
    """
    Import a dotted module path and return the attribute/class designated by the
    last name in the path. Raise ImportError if the import failed.
    """
    try:
        module_path, class_name = dotted_path.rsplit('.', 1)
    except ValueError:
        msg = "%s doesn't look like a module path" % dotted_path
        six.reraise(ImportError, ImportError(msg), sys.exc_info()[2])

    module = import_module(module_path)
    try:
        return getattr(module, class_name)
    except AttributeError:
        msg = 'Module "%s" does not define a "%s" attribute/class' % (
         module_path, class_name)
        six.reraise(ImportError, ImportError(msg), sys.exc_info()[2])


def autodiscover_modules(*args, **kwargs):
    """
    Auto-discover INSTALLED_APPS modules and fail silently when
    not present. This forces an import on them to register any admin bits they
    may want.

    You may provide a register_to keyword parameter as a way to access a
    registry. This register_to object must have a _registry instance variable
    to access it.
    """
    from django.apps import apps
    register_to = kwargs.get('register_to')
    for app_config in apps.get_app_configs():
        for module_to_search in args:
            try:
                if register_to:
                    before_import_registry = copy.copy(register_to._registry)
                import_module('%s.%s' % (app_config.name, module_to_search))
            except Exception:
                if register_to:
                    register_to._registry = before_import_registry
                if module_has_submodule(app_config.module, module_to_search):
                    raise


if six.PY3:
    from importlib.util import find_spec as importlib_find

    def module_has_submodule(package, module_name):
        """See if 'module' is in 'package'."""
        try:
            package_name = package.__name__
            package_path = package.__path__
        except AttributeError:
            return False

        full_module_name = package_name + '.' + module_name
        return importlib_find(full_module_name, package_path) is not None


else:
    import imp

    def module_has_submodule(package, module_name):
        """See if 'module' is in 'package'."""
        name = ('.').join([package.__name__, module_name])
        try:
            return sys.modules[name] is not None
        except KeyError:
            pass

        try:
            package_path = package.__path__
        except AttributeError:
            return False

        for finder in sys.meta_path:
            if finder.find_module(name, package_path):
                return True

        for entry in package_path:
            try:
                finder = sys.path_importer_cache[entry]
                if finder is None:
                    try:
                        file_, _, _ = imp.find_module(module_name, [entry])
                        if file_:
                            file_.close()
                        return True
                    except ImportError:
                        continue

                else:
                    if finder.find_module(name):
                        return True
                    continue
            except KeyError:
                for hook in sys.path_hooks:
                    try:
                        finder = hook(entry)
                        if finder.find_module(name):
                            return True
                        break
                    except ImportError:
                        continue

                else:
                    if os.path.isdir(entry):
                        try:
                            file_, _, _ = imp.find_module(module_name, [entry])
                            if file_:
                                file_.close()
                            return True
                        except ImportError:
                            pass

        else:
            return False

        return


def module_dir(module):
    """
    Find the name of the directory that contains a module, if possible.

    Raise ValueError otherwise, e.g. for namespace packages that are split
    over several directories.
    """
    paths = list(getattr(module, '__path__', []))
    if len(paths) == 1:
        return paths[0]
    else:
        filename = getattr(module, '__file__', None)
        if filename is not None:
            return os.path.dirname(filename)
        raise ValueError('Cannot determine directory containing %s' % module)
        return