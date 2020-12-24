# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ice/adverlet/metadirectives.py
# Compiled at: 2008-12-22 07:00:12
__license__ = 'GPL v.3'
__docformat__ = 'restructuredtext'
from zope.interface import Interface
from zope.schema import TextLine, Text, Bool

class IAdverletDirective(Interface):
    """ Defines adverlet """
    __module__ = __name__
    name = TextLine(title='Name', description='Adverlets is looked up by the name', required=True)
    description = Text(title='Description', description='Useful description for content manager', required=False)
    default = TextLine(title='Default view name', description='Default view name', required=False)
    wysiwyg = Bool(title='Rich-text editor by default', description='Rich-text editor not always useful', required=False, default=True)