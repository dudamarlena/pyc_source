# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/blog/paragraph.py
# Compiled at: 2012-06-26 16:33:07
__docformat__ = 'restructuredtext'
from persistent import Persistent
from ztfy.blog.interfaces.paragraph import IParagraph
from zope.container.contained import Contained
from zope.interface import implements
from zope.schema.fieldproperty import FieldProperty
from ztfy.i18n.property import I18nTextProperty

class Paragraph(Persistent, Contained):
    implements(IParagraph)
    title = I18nTextProperty(IParagraph['title'])
    heading = I18nTextProperty(IParagraph['heading'])
    visible = FieldProperty(IParagraph['visible'])