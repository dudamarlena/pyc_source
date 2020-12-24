# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hvelarde/collective/sc.photogallery/src/sc/photogallery/tiles/photogallery.py
# Compiled at: 2017-10-20 17:03:39
from collective.cover.tiles.base import IPersistentCoverTile
from collective.cover.tiles.base import PersistentCoverTile
from plone.app.uuid.utils import uuidToObject
from plone.memoize import view
from plone.tiles.interfaces import ITileDataManager
from plone.uuid.interfaces import IUUID
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from sc.photogallery import _
from sc.photogallery.utils import PhotoGalleryMixin
from zope import schema
from zope.interface import implementer

class IPhotoGalleryTile(IPersistentCoverTile):
    """A tile that shows a photo gallery."""
    uuid = schema.TextLine(title=_('UUID'), required=False, readonly=True)


@implementer(IPhotoGalleryTile)
class PhotoGalleryTile(PersistentCoverTile, PhotoGalleryMixin):
    """A tile that shows a photo gallery."""
    index = ViewPageTemplateFile('photogallery.pt')
    is_configurable = True
    is_editable = False
    is_droppable = True
    short_name = _('msg_short_name_photogallery', 'Photo Gallery')

    def accepted_ct(self):
        """Accept only Photo Gallery objects."""
        return [
         'Photo Gallery']

    def populate_with_object(self, obj):
        super(PhotoGalleryTile, self).populate_with_object(obj)
        if obj.portal_type in self.accepted_ct():
            uuid = IUUID(obj)
            data_mgr = ITileDataManager(self)
            data_mgr.set(dict(uuid=uuid))

    def is_empty(self):
        return self.data.get('uuid', None) is None or uuidToObject(self.data.get('uuid')) is None

    @view.memoize
    def gallery(self):
        return uuidToObject(self.data.get('uuid'))

    @view.memoize
    def results(self):
        gallery = self.gallery()
        return gallery.listFolderContents()

    def image(self, obj, scale='large'):
        """Return an image scale if the item has an image field.

        :param obj: [required]
        :type obj: content type object
        :param scale: the scale to be used
        :type scale: string
        """
        scales = obj.restrictedTraverse('@@images')
        return scales.scale('image', scale)