# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tpDcc/dccs/maya/register.py
# Compiled at: 2020-05-02 23:38:23
# Size of source mod 2**32: 890 bytes
"""
Register module for tpDcc-dccs-maya
"""
from __future__ import print_function, division, absolute_import
__author__ = 'Tomas Poveda'
__license__ = 'MIT'
__maintainer__ = 'Tomas Poveda'
__email__ = 'tpovedatd@gmail.com'

def register_class(cls_name, cls, is_unique=False):
    """
    This function registers given class into tpRigToolkit module
    :param cls_name: str, name of the class we want to register
    :param cls: class, class we want to register
    :param is_unique: bool, Whether if the class should be updated if new class is registered with the same name
    """
    import tpDcc.dccs.maya
    if is_unique:
        if cls_name in tpDcc.dccs.maya.__dict__:
            setattr(tpDcc.dccs.maya.__dict__, cls_name, getattr(tpDcc.dccs.maya.__dict__, cls_name))
    else:
        tpDcc.dccs.maya.__dict__[cls_name] = cls