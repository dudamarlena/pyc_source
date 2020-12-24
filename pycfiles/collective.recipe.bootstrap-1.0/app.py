# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/aclark/Developer/collective/collective.recipe.bluebream/collective/recipe/bluebream/welcome/app.py
# Compiled at: 2012-04-08 15:58:16
from zope.interface import implements
from zope.site.folder import Folder
from interfaces import ISampleApplication

class SampleApplication(Folder):
    implements(ISampleApplication)
    name = ''
    description = ''