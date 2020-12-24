# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/runner/runners/2.169.1/work/MetaWards/MetaWards/tests/../build/lib.macosx-10.14-x86_64-3.7/metawards/mixers/_mix_default.py
# Compiled at: 2020-05-11 13:26:49
# Size of source mod 2**32: 228 bytes
__all__ = ['mix_default']

def mix_default(**kwargs):
    """This is the default mixer. By default, nothing extra is mixed
       at any stage of the model run
    """
    from ._mix_none import mix_none
    return mix_none()