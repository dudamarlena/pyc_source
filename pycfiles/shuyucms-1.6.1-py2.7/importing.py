# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/shuyucms/utils/importing.py
# Compiled at: 2016-02-29 22:16:54
from __future__ import unicode_literals
import os
from django.utils.importlib import import_module

def path_for_import(name):
    """
    Returns the directory path for the given package or module.
    """
    return os.path.dirname(os.path.abspath(import_module(name).__file__))


def import_dotted_path(path):
    """
    Takes a dotted path to a member name in a module, and returns
    the member after importing it.
    """
    try:
        module_path, member_name = path.rsplit(b'.', 1)
        module = import_module(module_path)
        return getattr(module, member_name)
    except (ValueError, ImportError, AttributeError) as e:
        raise ImportError(b'Could not import the name: %s: %s' % (path, e))