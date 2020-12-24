# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/ocfl/__init__.py
# Compiled at: 2020-04-20 18:53:01
# Size of source mod 2**32: 386 bytes
"""Python implementation of OCFL."""
import sys
from .object import *
from .version import *
from .store import *
from .digest import *
from .disposition import get_dispositor
from .bagger import bag_as_source, bag_extracted_version, BaggerError
__version__ = '0.0.3'
if sys.version_info < (2, 7):
    raise Exception('Must use python 2.7 or greater (probably)!')