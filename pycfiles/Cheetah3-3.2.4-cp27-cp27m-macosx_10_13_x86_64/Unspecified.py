# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/lib.macosx-10.13-x86_64-2.7/Cheetah/Unspecified.py
# Compiled at: 2019-09-22 10:12:27
try:
    from ds.sys.Unspecified import Unspecified
except ImportError:

    class _Unspecified:

        def __repr__(self):
            return 'Unspecified'

        def __str__(self):
            return 'Unspecified'


    Unspecified = _Unspecified()