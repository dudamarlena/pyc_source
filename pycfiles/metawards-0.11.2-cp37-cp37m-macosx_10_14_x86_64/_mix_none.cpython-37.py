# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/runner/runners/2.169.1/work/MetaWards/MetaWards/tests/../build/lib.macosx-10.14-x86_64-3.7/metawards/mixers/_mix_none.py
# Compiled at: 2020-05-11 13:26:49
# Size of source mod 2**32: 251 bytes
__all__ = ['mix_none']

def mix_none(**kwargs):
    """This mixer will perform no mixing. The result is that
       the demographics won't interact with one another and
       each disease outbreak will be completely separate.
    """
    return []