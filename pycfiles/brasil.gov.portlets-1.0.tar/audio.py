# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/hvelarde/forcontent/idg/src/brasil.gov.portal/src/brasil/gov/portal/content/audio.py
# Compiled at: 2018-10-18 17:35:13
__doc__ = "Audio content type and subscribers associated with it.\n\nAn Audio is a container of audio formats: MP3 (MPEGAudioFile) and\nVorbis (OGGAudioFile) and can only hold one file of each format,\nthat's is handled by a couple of subscribers.\n"
from brasil.gov.portal.content.audio_file import IMPEGAudioFile
from brasil.gov.portal.content.audio_file import IOGGAudioFile
from plone.dexterity.content import Container
from zope.interface import implementer
from zope.interface import Interface

class IAudio(Interface):
    """An Audio (in fact a container of audio formats)."""


@implementer(IAudio)
class Audio(Container):

    def return_ogg(self):
        """Return the Vorbis version of the audio."""
        sources = self.objectValues()
        for source in sources:
            if IOGGAudioFile.providedBy(source):
                return source

    def return_mp3(self):
        """Return the MP3 version of the audio."""
        sources = self.objectValues()
        for source in sources:
            if IMPEGAudioFile.providedBy(source):
                return source


def object_added(obj, event):
    """Remove further permission to add a file type after adding it."""
    parent = event.newParent
    if IAudio.providedBy(parent):
        if IMPEGAudioFile.providedBy(obj):
            permission = 'brasil.gov.portal: Add MPEG File'
        elif IOGGAudioFile.providedBy(obj):
            permission = 'brasil.gov.portal: Add OGG File'
        if permission:
            parent.manage_permission(permission, roles=[], acquire=0)


def object_removed(obj, event):
    """Grant permission to add a file type after removing it."""
    parent = event.oldParent
    if IAudio.providedBy(parent):
        if IMPEGAudioFile.providedBy(obj):
            permission = 'brasil.gov.portal: Add MPEG File'
        elif IOGGAudioFile.providedBy(obj):
            permission = 'brasil.gov.portal: Add OGG File'
        if permission:
            parent.manage_permission(permission, roles=[], acquire=1)