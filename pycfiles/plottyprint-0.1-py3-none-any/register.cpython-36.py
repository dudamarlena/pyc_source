# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/plottwist/register.py
# Compiled at: 2020-04-15 09:53:56
# Size of source mod 2**32: 829 bytes
__doc__ = '\nRegister module for plottwist\n'
from __future__ import print_function, division, absolute_import
__author__ = 'Tomas Poveda'
__license__ = 'MIT'
__maintainer__ = 'Tomas Poveda'
__email__ = 'tpovedatd@gmail.com'

def register_class(cls_name, cls, is_unique=False):
    """
    This function registers given class
    :param cls_name: str, name of the class we want to register
    :param cls: class, class we want to register
    :param is_unique: bool, Whether if the class should be updated if new class is registered with the same name
    """
    import plottwist
    if is_unique:
        if cls_name in plottwist.__dict__:
            setattr(plottwist.__dict__, cls_name, getattr(plottwist.__dict__, cls_name))
    else:
        plottwist.__dict__[cls_name] = cls