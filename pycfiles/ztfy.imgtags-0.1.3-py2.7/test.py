# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/imgtags/browser/test.py
# Compiled at: 2012-06-21 08:42:14
from persistent import Persistent
from ztfy.imgtags.interfaces import IImageTags
from z3c.form import field
from zope.container.contained import Contained
from zope.interface import implements, Interface
from zope.schema import TextLine
from zope.schema.fieldproperty import FieldProperty
from zope.traversing.browser.absoluteurl import absoluteURL
from ztfy.extfile.blob import BlobImage
from ztfy.file.property import ImageProperty
from ztfy.file.schema import ImageField
from ztfy.skin.form import AddForm, EditForm, DisplayForm
from ztfy.skin.menu import MenuItem
from ztfy.imgtags import _

class IImageTagsTest(Interface):
    """Image tags test interface"""
    title = TextLine(title='Title', required=True)
    image = ImageField(title=_('Image data'), required=True)


class ImageTagsTest(Persistent, Contained):
    """Image tags test class"""
    implements(IImageTagsTest)
    title = FieldProperty(IImageTagsTest['title'])
    image = ImageProperty(IImageTagsTest['image'], klass=BlobImage)


class ImageTagsTestAddFormMenuItem(MenuItem):
    """Image tags test add menu item"""
    title = ':: Add image tags test...'


class ImageTagsTestAddForm(AddForm):
    """Image tags test add form"""
    fields = field.Fields(IImageTagsTest)

    def create(self, data):
        img = ImageTagsTest()
        img.title = data.get('title')
        return img

    def add(self, object):
        self.context[object.title] = object

    def nextURL(self):
        return '%s/@@contents.html' % absoluteURL(self.context, self.request)


class ImageTagsTestEditForm(EditForm):
    """Image tags test edit form"""
    fields = field.Fields(IImageTagsTest)


class ImageTagsTestTagsDisplayFormMenuItem(MenuItem):
    """Image tags test add menu item"""
    title = 'EXIF/IPTC/XMP tags'


class ImageTagsTestTagsDisplayForm(DisplayForm):
    """Image tags test tags display form"""
    fields = field.Fields(Interface)

    @property
    def tags(self):
        return IImageTags(self.context.image)