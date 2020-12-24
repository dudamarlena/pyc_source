# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: c:\git\pydicom-clean\source\build\lib\dicom\tagtools.py
# Compiled at: 2017-01-26 21:08:30
# Size of source mod 2**32: 472 bytes
""" Tools to wrap dataset tag operations

Usage:

    for tag in ds.keys():
        with valid_tag(tag):
            # Anything that goes wrong here is annotated
 """
from contextlib import contextmanager

@contextmanager
def tag_in_exception(tag):
    """ Perform a protected read on the tag """
    try:
        yield
    except Exception as e:
        err = 'Invalid tag {0}: {1}'
        err = err.format(tag, str(e))
        raise type(e)(err)