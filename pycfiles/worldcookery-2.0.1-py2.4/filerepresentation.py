# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.darwin-8.8.2-i386/egg/worldcookery/filerepresentation.py
# Compiled at: 2006-09-21 05:27:36
from zope.interface import implements
from zope.component import adapts
from zope.filerepresentation.interfaces import IReadFile, IWriteFile
from zope.filerepresentation.interfaces import IFileFactory
from worldcookery.recipe import Recipe
from worldcookery.interfaces import IRecipe

class RecipeReadFile(object):
    __module__ = __name__
    implements(IReadFile)
    adapts(IRecipe)

    def __init__(self, context):
        self.context = context
        self.data = self.context.description.encode('utf-8')

    def read(self):
        return self.data

    def size(self):
        return len(self.data)


class RecipeWriteFile(object):
    __module__ = __name__
    implements(IWriteFile)
    adapts(IRecipe)

    def __init__(self, context):
        self.context = context

    def write(self, data):
        self.context.description = data.decode('utf-8')


from worldcookery.interfaces import IRecipeContainer

class RecipeFactory(object):
    __module__ = __name__
    implements(IFileFactory)
    adapts(IRecipeContainer)

    def __init__(self, context):
        self.context = context

    def __call__(self, name, content_type, data):
        recipe = Recipe()
        recipe.name = name.title()
        recipe.description = data.decode('utf-8')
        return recipe


from zope.filerepresentation.interfaces import IDirectoryFactory
from zope.exceptions.interfaces import UserError

class RecipeDirectoryFactory(object):
    __module__ = __name__
    implements(IDirectoryFactory)
    adapts(IRecipeContainer)

    def __init__(self, context):
        self.context = context

    def __call__(self, name):
        raise UserError('Cannot create subfolders in recipe folders.')