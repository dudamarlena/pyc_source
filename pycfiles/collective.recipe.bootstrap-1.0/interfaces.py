# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/aclark/Developer/collective/collective.recipe.bluebream/collective/recipe/bluebream/welcome/interfaces.py
# Compiled at: 2012-04-08 15:58:16
from zope.site.interfaces import IFolder
from zope.schema import TextLine
from zope.schema import Text

class ISampleApplication(IFolder):
    """The main application container."""
    name = TextLine(title='Name', description='Name of application.', default='', required=True)
    description = Text(title='Description', description='The name of application container.', default='', required=False)