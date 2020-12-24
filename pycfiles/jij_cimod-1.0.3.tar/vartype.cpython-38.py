# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/ssd/workspace/linux/workspace/Jij/cimod/cimod/vartype.py
# Compiled at: 2020-04-28 17:44:22
# Size of source mod 2**32: 981 bytes
import cxxcimod, dimod
SPIN = dimod.SPIN
BINARY = dimod.BINARY
Vartype = dimod.Vartype

def to_cxxcimod(var_type):
    if isinstance(var_type, cxxcimod.Vartype):
        return var_type
    var_type = dimod.as_vartype(var_type)
    if var_type == dimod.SPIN:
        return cxxcimod.Vartype.SPIN
    if var_type == dimod.BINARY:
        return cxxcimod.Vartype.BINARY