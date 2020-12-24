# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/wc/sqlrecipe/folder.py
# Compiled at: 2007-09-29 16:14:39
from zope.interface import implements
from z3c.zalchemy.container import SQLAlchemyContainer
from worldcookery.interfaces import IRecipeContainer

class RecipeFolder(SQLAlchemyContainer):
    __module__ = __name__
    implements(IRecipeContainer)

    def __init__(self):
        self.className = 'wc.sqlrecipe.recipe.Recipe'