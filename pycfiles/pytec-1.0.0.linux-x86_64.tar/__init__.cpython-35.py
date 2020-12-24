# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /media/storage/eyes/virtualenv/pyte/lib/python3.5/site-packages/pyte/__init__.py
# Compiled at: 2016-04-17 12:52:06
# Size of source mod 2**32: 988 bytes
"""
Pyte package file, import some useful stuff from other functions.
"""
import sys
__version__ = '1.0.0'
if sys.version_info[1] == 2:
    from . import tokens_32 as tokens
else:
    if sys.version_info[1] == 3:
        from . import tokens_33 as tokens
    else:
        if sys.version_info[1] == 4:
            from . import tokens_34 as tokens
        elif sys.version_info[1] == 5:
            from . import tokens_35 as tokens
from .compiler import compile
from . import superclasses
from . import ops

def _create_validated(*args, name) -> superclasses.PyteAugmentedArgList:
    return superclasses.PyteAugmentedArgList(args, name=name)


def create_names(*args) -> superclasses.PyteAugmentedArgList:
    return _create_validated(*args, name='names')


def create_consts(*args) -> superclasses.PyteAugmentedArgList:
    return _create_validated(*args, name='consts')


def create_varnames(*args) -> superclasses.PyteAugmentedArgList:
    return _create_validated(*args, name='varnames')