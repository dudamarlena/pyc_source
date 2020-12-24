# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/blog/paragraphs/illustration.py
# Compiled at: 2012-06-26 16:33:07
__docformat__ = 'restructuredtext'
from ztfy.blog.paragraphs.interfaces import IIllustration
from zope.interface import implements
from zope.schema.fieldproperty import FieldProperty
from ztfy.blog.paragraph import Paragraph
from ztfy.extfile.blob import BlobImage
from ztfy.i18n.property import I18nImageProperty

class Illustration(Paragraph):
    implements(IIllustration)
    body = I18nImageProperty(IIllustration['body'], klass=BlobImage, img_klass=BlobImage)
    position = FieldProperty(IIllustration['position'])
    display_width = FieldProperty(IIllustration['display_width'])
    break_after = FieldProperty(IIllustration['break_after'])
    zoomable = FieldProperty(IIllustration['zoomable'])
    zoom_width = FieldProperty(IIllustration['zoom_width'])