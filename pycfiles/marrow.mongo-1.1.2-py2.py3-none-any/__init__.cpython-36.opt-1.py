# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /marrow/mongo/__init__.py
# Compiled at: 2017-05-17 14:49:33
# Size of source mod 2**32: 608 bytes
from __future__ import unicode_literals
import sys
from .core import Document, Field, Index, __version__
from .query import Q, Ops, Filter, Update
from .param import F, P, S, U
from .util import Registry, utcnow
document = sys.modules['marrow.mongo.document'] = Registry('marrow.mongo.document')
field = sys.modules['marrow.mongo.field'] = Registry('marrow.mongo.field')
trait = sys.modules['marrow.mongo.trait'] = Registry('marrow.mongo.trait')
__all__ = [
 'Document',
 'F',
 'Field',
 'Filter',
 'Index',
 'Ops',
 'P',
 'Q',
 'S',
 'U',
 'Update',
 'document',
 'field']