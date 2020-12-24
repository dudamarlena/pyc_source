# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/wc/textpage/interfaces.py
# Compiled at: 2007-02-23 15:42:05
from zope.interface import Interface
from zope.schema import SourceText, Choice
from zope.i18nmessageid import MessageFactory
_ = MessageFactory('wc.textpage')

class IPage(Interface):
    """A very very simple page."""
    __module__ = __name__
    text = SourceText(title=_('Text'), description=_('Text of the page.'), default='', required=True)
    type = Choice(title=_('Text type'), description=_('Type of the text, e.g. structured text'), default='zope.source.rest', required=True, vocabulary='SourceTypes')