# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Applications/Plone/zinstance/src/collective.ptg.tile/collective/ptg/tile/ptg_tile.py
# Compiled at: 2014-02-04 07:34:47
from plone import tiles
from zope.interface import Interface
from Acquisition import aq_inner
from collective.cover import _
from collective.cover.tiles.base import AnnotationStorage
from collective.cover.tiles.base import IPersistentCoverTile
from collective.cover.tiles.base import PersistentCoverTile
from plone.tiles.interfaces import ITileDataManager
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.interface import implements
import time
from plone.app.uuid.utils import uuidToObject
from plone.tiles.interfaces import ITileDataManager
from plone.uuid.interfaces import IUUID
from zope import schema
from plone import api
from plone.memoize.instance import memoize

class IPtgTile(IPersistentCoverTile):
    """  settings for gallery  tile """
    title = schema.TextLine(title=_('Title'), required=False)
    description = schema.Text(title=_('Description'), required=False)
    gallerypath = schema.Choice(title=_('label_width_title_gallerytile_setting', default='Gallery'), description=_('label_width_description_gallerytile_setting', default='The path to the gallery you want to  show.'), vocabulary='collective.ptg.tile.GalleryVocabulary')


class PtgTile(PersistentCoverTile):
    implements(IPtgTile)
    index = ViewPageTemplateFile('ptg_tile.pt')
    is_configurable = True

    def is_set(self):
        return self.data['gallerypath']

    def gallerypath(self):
        portal = api.portal.get()
        path = str(self.data['gallerypath'])
        if path.startswith('/'):
            path = path[1:]
        return portal.restrictedTraverse(path, default=False)