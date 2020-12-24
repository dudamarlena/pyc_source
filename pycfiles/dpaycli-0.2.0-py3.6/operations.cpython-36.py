# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/dpaycligraphenebase/operations.py
# Compiled at: 2018-10-14 09:33:48
# Size of source mod 2**32: 1037 bytes
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from collections import OrderedDict
import json
from .types import Uint8, Int16, Uint16, Uint32, Uint64, Varint32, Int64, String, Bytes, Void, Array, PointInTime, Signature, Bool, Set, Fixed_array, Optional, Static_variant, Map, Id
from .objects import GrapheneObject, isArgsThisClass
from .account import PublicKey
from .chains import default_prefix
from .objects import Operation
from .operationids import operations

class Demooepration(GrapheneObject):

    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1:
                if len(kwargs) == 0:
                    kwargs = args[0]
            super(Demooepration, self).__init__(OrderedDict([
             (
              'string', String(kwargs['string'], 'account')),
             (
              'extensions', Set([]))]))