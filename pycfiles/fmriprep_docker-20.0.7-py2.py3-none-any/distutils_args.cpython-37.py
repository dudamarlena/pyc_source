# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-aejasjrz/pip/pip/_internal/utils/distutils_args.py
# Compiled at: 2020-05-05 12:41:47
# Size of source mod 2**32: 1350 bytes
from distutils.errors import DistutilsArgError
from distutils.fancy_getopt import FancyGetopt
from pip._internal.utils.typing import MYPY_CHECK_RUNNING
if MYPY_CHECK_RUNNING:
    from typing import Dict, List
_options = [
 ('exec-prefix=', None, ''),
 ('home=', None, ''),
 ('install-base=', None, ''),
 ('install-data=', None, ''),
 ('install-headers=', None, ''),
 ('install-lib=', None, ''),
 ('install-platlib=', None, ''),
 ('install-purelib=', None, ''),
 ('install-scripts=', None, ''),
 ('prefix=', None, ''),
 ('root=', None, ''),
 ('user', None, '')]
_distutils_getopt = FancyGetopt(_options)

def parse_distutils_args(args):
    """Parse provided arguments, returning an object that has the
    matched arguments.

    Any unknown arguments are ignored.
    """
    result = {}
    for arg in args:
        try:
            _, match = _distutils_getopt.getopt(args=[arg])
        except DistutilsArgError:
            pass
        else:
            result.update(match.__dict__)

    return result