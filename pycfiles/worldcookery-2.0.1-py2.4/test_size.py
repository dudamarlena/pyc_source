# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.darwin-8.8.2-i386/egg/worldcookery/tests/test_size.py
# Compiled at: 2006-09-21 05:27:35
import unittest
from zope.i18n import translate
from worldcookery.recipe import Recipe
from worldcookery.size import RecipeSize

class RecipeSizeTestCase(unittest.TestCase):
    __module__ = __name__

    def setUp(self):
        self.recipe = recipe = Recipe()
        recipe.name = 'Fish and Chips'
        recipe.ingredients = ['Fish', 'Potato chips']
        recipe.description = 'Fish and Chips is a typical British dish.'
        self.size = RecipeSize(recipe)

    def test_size_for_sorting(self):
        (unit, size) = self.size.sizeForSorting()
        self.assertEqual(unit, 'byte')
        self.assertEqual(size, 71)

    def test_size_for_display(self):
        msg = self.size.sizeForDisplay()
        self.assertEqual('71 characters', translate(msg))


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(RecipeSizeTestCase))
    return suite


if __name__ == '__main__':
    unittest.main()