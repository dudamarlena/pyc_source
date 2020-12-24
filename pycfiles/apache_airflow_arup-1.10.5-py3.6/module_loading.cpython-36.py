# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/utils/module_loading.py
# Compiled at: 2019-09-11 02:44:38
# Size of source mod 2**32: 1478 bytes
from importlib import import_module

def import_string(dotted_path):
    """
    Import a dotted module path and return the attribute/class designated by the
    last name in the path. Raise ImportError if the import failed.
    """
    try:
        module_path, class_name = dotted_path.rsplit('.', 1)
    except ValueError:
        raise ImportError("{} doesn't look like a module path".format(dotted_path))

    module = import_module(module_path)
    try:
        return getattr(module, class_name)
    except AttributeError:
        raise ImportError('Module "{}" does not define a "{}" attribute/class'.format(module_path, class_name))