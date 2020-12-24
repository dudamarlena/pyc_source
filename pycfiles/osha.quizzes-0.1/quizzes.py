# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/zupo/work/osha.quizzes/src/osha/quizzes/browser/quizzes.py
# Compiled at: 2012-10-18 09:44:55
"""A Folder view that lists Todo Items."""
from five import grok
from Products.ATContentTypes.interface import IATFolder
grok.templatedir('.')

class Quizzes(grok.View):
    """A BrowserView to display the Quizzes listing on a Folder."""
    grok.context(IATFolder)
    grok.require('zope2.View')