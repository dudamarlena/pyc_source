# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/test/bibliopixel/project/types/base.py
# Compiled at: 2019-08-11 12:22:47
# Size of source mod 2**32: 331 bytes
import unittest
from bibliopixel.project import fields

class TypesBaseTest(unittest.TestCase):

    def make(self, name, c, result=None):
        component = fields.component({name: c}, field_types=(fields.FIELD_TYPES))
        if result is not None:
            self.assertEqual(component, {name: result})
        return component