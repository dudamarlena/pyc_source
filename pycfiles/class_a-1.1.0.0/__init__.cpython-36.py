# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/mannatsingh/dev/git/upstream/ClassyVision/classy_vision/templates/synthetic/models/__init__.py
# Compiled at: 2020-04-29 11:26:04
# Size of source mod 2**32: 437 bytes
from pathlib import Path
from classy_vision.generic.registry_utils import import_all_modules
FILE_ROOT = Path(__file__).parent
import_all_modules(FILE_ROOT, 'models')