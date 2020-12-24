# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/galaxy/util/image_util.py
# Compiled at: 2018-04-20 03:19:42
"""Provides utilities for working with image files."""
from __future__ import absolute_import
import imghdr, logging
try:
    import Image as PIL
except ImportError:
    try:
        from PIL import Image as PIL
    except ImportError:
        PIL = None

log = logging.getLogger(__name__)

def image_type(filename):
    fmt = None
    if PIL is not None:
        try:
            im = PIL.open(filename)
            fmt = im.format
            im.close()
        except Exception:
            pass

    if not fmt:
        fmt = imghdr.what(filename)
    if fmt:
        return fmt.upper()
    else:
        return False
        return


def check_image_type(filename, types):
    fmt = image_type(filename)
    if fmt in types:
        return True
    return False