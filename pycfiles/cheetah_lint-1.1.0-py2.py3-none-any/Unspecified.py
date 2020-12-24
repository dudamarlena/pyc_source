# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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