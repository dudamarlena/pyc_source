# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hvelarde/collective/sc.photogallery/src/sc/photogallery/controlpanel.py
# Compiled at: 2017-10-20 16:05:59
from plone.app.registry.browser import controlpanel
from sc.photogallery import _
from sc.photogallery.interfaces import IPhotoGallerySettings

class PhotoGallerySettingsEditForm(controlpanel.RegistryEditForm):
    """Control panel edit form."""
    schema = IPhotoGallerySettings
    label = _('Photo Gallery')
    description = _('Settings for the sc.photogallery package')


class PhotoGallerySettingsControlPanel(controlpanel.ControlPanelFormWrapper):
    """Control panel form wrapper."""
    form = PhotoGallerySettingsEditForm