# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mannatsingh/dev/git/upstream/ClassyVision/classy_vision/templates/synthetic/models/__init__.py
# Compiled at: 2020-04-29 11:26:04
# Size of source mod 2**32: 437 bytes
from pathlib import Path
from classy_vision.generic.registry_utils import import_all_modules
FILE_ROOT = Path(__file__).parent
import_all_modules(FILE_ROOT, 'models')