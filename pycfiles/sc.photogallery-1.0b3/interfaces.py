# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hvelarde/collective/sc.photogallery/src/sc/photogallery/interfaces.py
# Compiled at: 2018-01-29 16:00:07
from plone.app.dexterity import MessageFactory as __
from plone.app.textfield import RichText
from plone.supermodel import model
from sc.photogallery import _
from zope import schema
from zope.interface import Interface

class IBrowserLayer(Interface):
    """Add-on layer marker interface."""
    pass


class IPhotoGallery(model.Schema):
    """A Photo Gallery content type with a slideshow view."""
    text = RichText(title=_('Body text'), required=False)
    model.fieldset('settings', label=__('Settings'), fields=['allow_download'])
    allow_download = schema.Bool(title=_('Allow image download?'), description=_('Allow downloading of original images on this photo gallery.'), default=True)


class IPhotoGallerySettings(model.Schema):
    """Schema for the control panel form."""
    enable_download = schema.Bool(title=_('Enable image download globally?'), description=_('Enable download of original images in photo galleries by using an explicit link. If ftw.zipexport is installed, enable also downloading of a ZIP file with all the images.'), default=False)