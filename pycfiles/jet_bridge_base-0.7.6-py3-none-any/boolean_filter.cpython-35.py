# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/f1nal/Dropbox/python/jet-bridge/src/packages/jet_bridge_base/jet_bridge_base/filters/boolean_filter.py
# Compiled at: 2020-03-04 16:40:12
# Size of source mod 2**32: 160 bytes
from jet_bridge_base.fields import BooleanField
from jet_bridge_base.filters.filter import Filter

class BooleanFilter(Filter):
    field_class = BooleanField