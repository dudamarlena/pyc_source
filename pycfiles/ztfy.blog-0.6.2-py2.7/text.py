# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/blog/paragraphs/text.py
# Compiled at: 2012-06-26 16:33:07
__docformat__ = 'restructuredtext'
from ztfy.blog.paragraphs.interfaces import ITextParagraph
from zope.interface import implements
from zope.schema.fieldproperty import FieldProperty
from ztfy.blog.paragraph import Paragraph
from ztfy.i18n.property import I18nTextProperty

class TextParagraph(Paragraph):
    implements(ITextParagraph)
    body = I18nTextProperty(ITextParagraph['body'])
    body_format = FieldProperty(ITextParagraph['body_format'])