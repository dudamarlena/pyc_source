# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.darwin-8.8.2-i386/egg/worldcookery/folder.py
# Compiled at: 2006-09-21 05:27:36
from zope.interface import implements
from zope.component import adapts
from zope.exceptions.interfaces import UserError
from zope.i18nmessageid import MessageFactory
_ = MessageFactory('worldcookery')
from zope.app.container.btree import BTreeContainer
from zope.app.container.contained import NameChooser
from worldcookery.interfaces import IRecipeContainer

class RecipeFolder(BTreeContainer):
    __module__ = __name__
    implements(IRecipeContainer)


class RecipeNameChooser(NameChooser):
    __module__ = __name__
    adapts(IRecipeContainer)

    def checkName(self, name, object):
        if name != object.name:
            raise UserError(_('Given name and recipe name do not match!'))
        return super(RecipeNameChooser, self).checkName(name, object)

    def chooseName(self, name, object):
        name = object.name
        self.checkName(name, object)
        return name