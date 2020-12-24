# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: c:\git\pydicom-clean\source\build\lib\dicom\test\version_dep.py
# Compiled at: 2017-01-26 21:08:30
# Size of source mod 2**32: 706 bytes
"""Holds test code that is dependent on certain python versions"""
import warnings

def capture_warnings(function, *func_args, **func_kwargs):
    """Capture function result and warnings.
    """
    with warnings.catch_warnings(record=True) as (w):
        warnings.simplefilter('always')
        result = function(*func_args, **func_kwargs)
        all_warnings = w
    return (
     result, [str(warning.message) for warning in all_warnings])