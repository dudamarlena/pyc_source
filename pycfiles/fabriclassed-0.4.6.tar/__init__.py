# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ramusus/workspace/movister/env/src/fabriclassed/fabriclassed/__init__.py
# Compiled at: 2015-03-02 01:19:54
from utils import add_class_methods_as_module_level_functions_for_fabric as initialize
VERSION = (0, 4, 6)
__version__ = ('.').join(map(str, VERSION))
__all__ = ['initialize']