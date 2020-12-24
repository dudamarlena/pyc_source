# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/aclark/Developer/collective/collective.recipe.bluebream/collective/recipe/bluebream/welcome/interfaces.py
# Compiled at: 2012-04-08 15:58:16
from zope.site.interfaces import IFolder
from zope.schema import TextLine
from zope.schema import Text

class ISampleApplication(IFolder):
    """The main application container."""
    name = TextLine(title='Name', description='Name of application.', default='', required=True)
    description = Text(title='Description', description='The name of application container.', default='', required=False)