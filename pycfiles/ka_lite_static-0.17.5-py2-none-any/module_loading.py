# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/django/django/utils/module_loading.py
# Compiled at: 2018-07-11 18:15:30
import imp, os, sys
from django.core.exceptions import ImproperlyConfigured
from django.utils import six
from django.utils.importlib import import_module

def import_by_path(dotted_path, error_prefix=''):
    """
    Import a dotted module path and return the attribute/class designated by the
    last name in the path. Raise ImproperlyConfigured if something goes wrong.
    """
    try:
        module_path, class_name = dotted_path.rsplit('.', 1)
    except ValueError:
        raise ImproperlyConfigured("%s%s doesn't look like a module path" % (
         error_prefix, dotted_path))

    try:
        module = import_module(module_path)
    except ImportError as e:
        msg = '%sError importing module %s: "%s"' % (
         error_prefix, module_path, e)
        six.reraise(ImproperlyConfigured, ImproperlyConfigured(msg), sys.exc_info()[2])

    try:
        attr = getattr(module, class_name)
    except AttributeError:
        raise ImproperlyConfigured('%sModule "%s" does not define a "%s" attribute/class' % (
         error_prefix, module_path, class_name))

    return attr


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