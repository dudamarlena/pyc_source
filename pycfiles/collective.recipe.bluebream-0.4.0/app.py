# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/aclark/Developer/collective/collective.recipe.bluebream/collective/recipe/bluebream/welcome/app.py
# Compiled at: 2012-04-08 15:58:16
from zope.interface import implements
from zope.site.folder import Folder
from interfaces import ISampleApplication

class SampleApplication(Folder):
    implements(ISampleApplication)
    name = ''
    description = ''