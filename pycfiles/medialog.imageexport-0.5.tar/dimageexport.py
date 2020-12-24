# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/espenmoe-nilssen/Plone/zinstance/src/medialog.imageexport/medialog/imageexport/browser/dimageexport.py
# Compiled at: 2016-04-04 06:53:57
import os, tempfile, zipfile
from Products.Five import BrowserView
from tempfile import TemporaryFile
from plone.dexterity.utils import iterSchemata, resolveDottedName
from zope.schema import getFields
from plone.dexterity.interfaces import IDexterityContent
from plone.namedfile.interfaces import IImageScaleTraversable, INamedImageField
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
try:
    from zope.app.component.hooks import getSite
except ImportError:
    from zope.component.hooks import getSite

from plone import api

class DExporter(BrowserView):
    """ Export full images from root """

    def render(self):
        return self.index()

    def __init__(self, context, request):
        super(DExporter, self).__init__(context, request)

    def __call__(self, REQUEST):
        self.export_images('full')

    def export_images(self, imagesize):
        """Returns zip file with images 
        """
        zip_filename = tempfile.mktemp()
        ZIP = zipfile.ZipFile(zip_filename, 'w')
        catalog = api.portal.get_tool(name='portal_catalog')
        folder_path = ('/').join(self.context.getPhysicalPath())
        brains = catalog(Language='', show_inactive=True, path={'query': folder_path, 'depth': -1})
        for obj in brains:
            obj = obj.getObject()
            try:
                try:
                    imageformat = obj.getContentType()
                    imageformat = imageformat.split('/')
                    image_suffix = imageformat[1]
                    if image_suffix == 'html':
                        image_suffix = 'jpg'
                    if image_suffix == 'jpeg':
                        image_suffix = 'jpg'
                    full_image_name = obj.getId() + '.' + image_suffix
                    img = obj.Schema().getField('image').getScale(obj, scale=imagesize)
                    ZIP.writestr(self.context.getId() + '/' + full_image_name, str(img.data))
                except:
                    if IDexterityContent.providedBy(obj):
                        for schemata in iterSchemata(obj):
                            for name, field in getFields(schemata).items():
                                if INamedImageField.providedBy(field):
                                    field_value = field.get(field.interface(obj))
                                    if field_value is not None:
                                        ZIP.writestr(self.context.getId() + '/' + str(field_value.filename.encode('utf8')), str(field_value.data))

            finally:
                pass

        ZIP.close()
        data = file(zip_filename).read()
        os.unlink(zip_filename)
        R = self.request.RESPONSE
        R.setHeader('content-type', 'application/zip')
        R.setHeader('content-length', len(data))
        R.setHeader('content-disposition', 'attachment; filename="%s.zip"' % self.context.getId())
        return R.write(data)