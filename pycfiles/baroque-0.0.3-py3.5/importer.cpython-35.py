# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/baroque/utils/importer.py
# Compiled at: 2017-03-22 15:29:51
# Size of source mod 2**32: 640 bytes
"""Utility functions for handling imports"""
import importlib

def class_from_dotted_path(dotted_path):
    """Loads a Python class from the supplied Python dot-separated class path.
    The class must be visible according to the PYTHONPATH variable contents.

    Example:
        ``"package.subpackage.module.MyClass" --> MyClass``

    Args:
        dotted_path (str): the dot-separated path of the class

    Returns:
        a ``type`` object

    """
    tokens = dotted_path.split('.')
    modpath, class_name = '.'.join(tokens[:-1]), tokens[(-1)]
    class_ = getattr(importlib.import_module(modpath), class_name)
    return class_