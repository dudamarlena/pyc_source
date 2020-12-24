# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/Dallinger/Dallinger/dallinger/patches.py
# Compiled at: 2020-04-26 19:37:24
# Size of source mod 2**32: 210 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar

def patch_ipython():
    try:
        from ipykernel.iostream import OutStream
    except ImportError:
        return
    else:
        OutStream.writable = lambda self: True


def patch():
    patch_ipython()