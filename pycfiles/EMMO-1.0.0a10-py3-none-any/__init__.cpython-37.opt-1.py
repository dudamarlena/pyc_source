# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /emmo/__init__.py
# Compiled at: 2020-04-27 16:37:38
# Size of source mod 2**32: 651 bytes
import sys
VERSION = '1.0.0-alpha-10'
if sys.version_info < (3, 6):
    raise RuntimeError('emmo requires Python 3.6 or later')
if 'owlready2' in sys.modules.keys():
    raise RuntimeError('emmo must be imported before owlready2')
from . import patch
from .ontology import World, get_ontology
from owlready2 import onto_path