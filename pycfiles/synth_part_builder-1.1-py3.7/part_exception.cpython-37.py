# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/synth_part_builder/part_exception.py
# Compiled at: 2019-06-19 10:12:06
# Size of source mod 2**32: 208 bytes
"""
    PartBuilder exception for part builder errors
"""

class PartBuilderException(Exception):
    __doc__ = '\n        Raised by PartBuilder functions when things go wrong\n    '