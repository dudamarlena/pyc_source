# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/gallery/paragraph.py
# Compiled at: 2012-06-26 16:39:45
__docformat__ = 'restructuredtext'
from ztfy.gallery.interfaces import IGalleryParagraph
from zope.interface import implements
from zope.schema.fieldproperty import FieldProperty
from ztfy.blog.paragraph import Paragraph

class GalleryParagraph(Paragraph):
    """Gallery link paragraph"""
    implements(IGalleryParagraph)
    renderer = FieldProperty(IGalleryParagraph['renderer'])