# uncompyle6 version 3.7.4
# Python bytecode 3.1 (3151)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dinoboff/Documents/workspace/skeleton/src/build/lib/skeleton/__init__.py
# Compiled at: 2010-05-11 17:49:21
"""
Basic Template system for project skeleton,
similar to the template part of PasteScript but without any dependencies.

"""
from skeleton.core import Skeleton, Var, Bool, FileNameKeyError, TemplateKeyError
from skeleton.utils import insert_into_file