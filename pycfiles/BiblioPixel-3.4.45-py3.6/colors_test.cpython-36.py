# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/test/bibliopixel/project/types/colors_test.py
# Compiled at: 2019-08-11 12:22:47
# Size of source mod 2**32: 973 bytes
from .base import TypesBaseTest
from bibliopixel.colors.palette import Palette

class ColorTypesTest(TypesBaseTest):

    def test_empty(self):
        self.make('colors', [], Palette())

    def test_single(self):
        self.make('colors', ['red'], Palette([(255, 0, 0)]))
        self.make('colors', 'red', Palette([(255, 0, 0)]))

    def test_many(self):
        self.make('colors', ['red', [0, 255, 0], 127], Palette([(255, 0, 0), (0, 255, 0), (127, 127, 127)]))

    def test_1d_list(self):
        self.make('colors', [0, 255, 0, 255, 0, 0, 23, 17], Palette([(0, 255, 0), (255, 0, 0)]))

    def test_dict(self):
        data = {'colors':[
          0, 255, 0, 255, 0, 0, 23, 17, 5], 
         'scale':2, 
         'serpentine':True}
        expected = Palette(colors=[
         (0, 255, 0), (255, 0, 0), (23, 17, 5)],
          scale=2,
          serpentine=True)
        self.make('colors', data, expected)