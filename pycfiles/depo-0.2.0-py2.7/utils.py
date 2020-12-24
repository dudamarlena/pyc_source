# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/depo/utils.py
# Compiled at: 2019-09-29 18:23:38
from __future__ import absolute_import, division, print_function
import json
from decimal import Decimal

class JSONEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, Decimal):
            return str(obj)
        else:
            return super(JSONEncoder, self).default(obj)