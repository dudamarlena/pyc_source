# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/wc/sqlrecipe/recipe.py
# Compiled at: 2007-09-29 16:14:39
from zope.interface import implements
from worldcookery.interfaces import IRecipe
from rwproperty import getproperty, setproperty

class Recipe(object):
    __module__ = __name__
    implements(IRecipe)
    __name__ = __parent__ = None
    name = ''
    time_to_cook = 0
    description = ''

    @getproperty
    def ingredients(self):
        return [ item.name for item in self._ingredients ]

    @setproperty
    def ingredients(self, new):
        existing = dict(((item.name, item) for item in self._ingredients))
        self._ingredients = [ existing.get(name, Ingredient(name)) for name in new ]

    @getproperty
    def tools(self):
        return [ item.name for item in self._tools ]

    @setproperty
    def tools(self, new):
        existing = dict(((item.name, item) for item in self._tools))
        self._tools = [ existing.get(name, KitchenTool(name)) for name in new ]


class Ingredient(object):
    __module__ = __name__

    def __init__(self, name):
        self.name = name


class KitchenTool(object):
    __module__ = __name__

    def __init__(self, name):
        self.name = name


from zope.component.factory import Factory
recipeFactory = Factory(Recipe, title='Create a new recipe', description='This factory instantiates new recipes.')
import sqlalchemy, z3c.zalchemy
recipe_table = sqlalchemy.Table('recipes', z3c.zalchemy.metadata('WorldCookery'), sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True), sqlalchemy.Column('name', sqlalchemy.Unicode), sqlalchemy.Column('time_to_cook', sqlalchemy.Integer), sqlalchemy.Column('description', sqlalchemy.Unicode))
ingredient_table = sqlalchemy.Table('ingredients', z3c.zalchemy.metadata('WorldCookery'), sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True), sqlalchemy.Column('recipe_id', sqlalchemy.Integer, sqlalchemy.ForeignKey('recipes.id')), sqlalchemy.Column('name', sqlalchemy.Unicode))
tool_table = sqlalchemy.Table('tools', z3c.zalchemy.metadata('WorldCookery'), sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True), sqlalchemy.Column('recipe_id', sqlalchemy.Integer, sqlalchemy.ForeignKey('recipes.id')), sqlalchemy.Column('name', sqlalchemy.Unicode))
sqlalchemy.mapper(Ingredient, ingredient_table)
sqlalchemy.mapper(KitchenTool, tool_table)
sqlalchemy.mapper(Recipe, recipe_table, properties={'_ingredients': sqlalchemy.relation(Ingredient, cascade='all, delete-orphan'), '_tools': sqlalchemy.relation(KitchenTool, cascade='all, delete-orphan')})