# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/brian/workspace/envs/envs/util.py
# Compiled at: 2016-12-13 15:43:22
# Size of source mod 2**32: 468 bytes
import sys, importlib

def import_mod(imp):
    """
    Lazily imports a module from a string
    @param imp:
    """
    __import__(imp, globals(), locals())
    return sys.modules[imp]


def import_util(imp):
    """
    Lazily imports a utils (class,
    function,or variable) from a module) from
    a string.
    @param imp:
    """
    mod_name, obj_name = imp.rsplit('.', 1)
    mod = importlib.import_module(mod_name)
    return getattr(mod, obj_name)