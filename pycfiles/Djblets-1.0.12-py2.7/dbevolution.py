# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/djblets/util/dbevolution.py
# Compiled at: 2019-06-12 01:17:17
from __future__ import unicode_literals
import warnings
from djblets.db.evolution import FakeChangeFieldType
from djblets.deprecation import RemovedInDjblets20Warning
warnings.warn(b'djblets.util.dbevolution is deprecated. Use djblets.db.evolution instead.', RemovedInDjblets20Warning)
__all__ = [
 b'FakeChangeFieldType']