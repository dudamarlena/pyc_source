# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/kipp3/exceptions.py
# Compiled at: 2019-12-16 21:55:05
# Size of source mod 2**32: 574 bytes
"""
---------------
Kipp Exceptions
---------------

KippException
  ├─ KippAIOException
  │    └─ KippAIOTimeoutError
  ├─ DBError
  │    ├─ DBValidateError
  │    ├─ DuplicateIndexError
  │    └─ RecordNotFound
  ├─ KippRunnerException
  │    └─ KippRunnerTimeoutException

"""
from __future__ import unicode_literals
from kipp3.libs.exceptions import KippAIOException, KippAIOTimeoutError, KippException
from kipp3.options import KippOptionsException, OptionKeyTypeConflictError