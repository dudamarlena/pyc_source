# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jhunk/Downloads/pandokia/pandokia/__init__.py
# Compiled at: 2018-06-11 11:14:06
# Size of source mod 2**32: 862 bytes
"""
bug: put a doc string here
describe pandokia.helpers, pandokia.runners

describe pandokia a little
"""
import os, sys
from .version import *
PY3 = bool(sys.hexversion >= 3145743)
if 'PDK_CONFIG' in os.environ:
    import pandokia.helpers.importer as i
    cfg = i.importer('pandokia.config', os.environ['PDK_CONFIG'])
else:
    import pandokia.default_config as cfg
never_expires = 2147483647