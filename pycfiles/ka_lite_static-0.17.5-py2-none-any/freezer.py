# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/South/south/tests/freezer.py
# Compiled at: 2018-07-11 18:15:31
from south.tests import unittest
from south.creator.freezer import model_dependencies
from south.tests.fakeapp import models

class TestFreezer(unittest.TestCase):

    def test_dependencies(self):
        self.assertEqual(set(model_dependencies(models.SubModel)), set([models.BaseModel, models.Other1, models.Other2]))
        self.assertEqual(set(model_dependencies(models.CircularA)), set([models.CircularA, models.CircularB, models.CircularC]))
        self.assertEqual(set(model_dependencies(models.Recursive)), set([models.Recursive]))