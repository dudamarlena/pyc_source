# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/csams/git_repos/personal/rulz/lib/python3.7/site-packages/rulz/loader.py
# Compiled at: 2019-05-11 13:34:23
# Size of source mod 2**32: 1901 bytes
import importlib, logging, os, pkgutil, re
log = logging.getLogger(__name__)

def _import(path, continue_on_error):
    log.debug(f"Importing {path}")
    try:
        return importlib.import_module(path)
    except Exception as ex:
        try:
            log.exception(ex)
            if not continue_on_error:
                raise
        finally:
            ex = None
            del ex


def _load(path, include='.*', exclude='test', continue_on_error=True):
    if path.endswith('.py'):
        path, _ = os.path.splitext(path)
    else:
        path = path.rstrip('/').replace('/', '.')
        package = _import(path, continue_on_error)
        if not package:
            return
        do_include = re.compile(include).search if include else (lambda x: True)
        do_exclude = re.compile(exclude).search if exclude else (lambda x: False)
        return hasattr(package, '__path__') or None
    prefix = package.__name__ + '.'
    for _, name, is_pkg in pkgutil.iter_modules(path=(package.__path__), prefix=prefix):
        if not name.startswith(prefix):
            name = prefix + name
        else:
            if is_pkg:
                _load(name, include, exclude, continue_on_error)
        if do_include(name):
            do_exclude(name) or _import(name, continue_on_error)


def load(*paths, **kwargs):
    """
    Each path in paths should be a full package or module name. They are
    recursively imported.

    Args:
        paths (str): A package or module to load

    Keyword Args:
        include (str): A regular expression of packages and modules to include.
            Defaults to '.*'
        exclude (str): A regular expression of packges and modules to exclude.
            Defaults to 'test'
        continue_on_error (bool): If True, continue importing even if something
            raises an ImportError. If False, raise the first ImportError.

    Raises:
        ImportError
    """
    for path in paths:
        _load(path, **kwargs)