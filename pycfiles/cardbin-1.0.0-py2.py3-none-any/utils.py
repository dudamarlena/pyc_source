# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.14-intel/egg/cardberg/utils.py
# Compiled at: 2019-10-03 03:22:15
from __future__ import absolute_import, division, print_function
import json
from decimal import Decimal

class JSONEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, Decimal):
            return str(obj)
        else:
            return super(JSONEncoder, self).default(obj)