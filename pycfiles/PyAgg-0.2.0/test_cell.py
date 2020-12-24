# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyage_forams/solutions/test_cell.py
# Compiled at: 2014-12-10 17:22:35
from unittest import TestCase
from pyage.core import inject
from pyage_forams.solutions.cell import Cell

class TestCell(TestCase):

    @classmethod
    def setUpClass(cls):
        super(TestCell, cls).setUpClass()
        inject.config = 'pyage_forams.conf.dummy_conf'

    def test_add_algae(self):
        cell = Cell()
        cell.add_algae(1000000)
        food = cell.available_food()
        cell.add_algae(1000000)
        self.assertEqual(food, cell.available_food())